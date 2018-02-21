import os
import json
import math
import argparse
import mdptoolbox
import numpy as np
import progressbar
import logging as log
from decimal import *


class MDP:
    """Convert the plain object description of the mdp into gamma and T and R matrices"""
    def __init__(self, descr):
        self.descr = descr
        self.gamma = descr["gamma"]
        self.nS = len(descr["states"])
        self.nA = len(descr["states"][0]["actions"])
        self.transitions = np.zeros((self.nA, self.nS, self.nS))
        self.rewards = np.zeros((self.nA, self.nS, self.nS))
        state_indexes = {state["id"]: i for i, state in enumerate(descr["states"])}
        for state in descr["states"]:
            assert len(state["actions"]) == self.nA, "All states must have same number of possible actions"
            for i, action in enumerate(state["actions"]):
                for transition in action["transitions"]:
                    state_index = state_indexes[state["id"]]
                    new_state_index = state_indexes[transition["to"]]
                    self.transitions[i, state_index, new_state_index] = transition["probability"]
                    self.rewards[i, state_index, new_state_index] = transition["reward"]

def get_iterations_with_mdptoolbox(mdp_descr):
    log.info('in get_iterations function')
    mdp = MDP(mdp_descr)

    log.info('running policy improvement')
    # (policy, v, it)
    results = []
    bar = progressbar.ProgressBar(maxval=1000,
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ',
                                           progressbar.Percentage()])
    bar.start()
    for t in range(1000):
        np.seterr(all='raise')
        try:
            initial_policy = np.random.choice(mdp.nA, size=mdp.nS)
            pi = mdptoolbox.mdp.PolicyIteration(
                mdp.transitions,
                mdp.rewards,
                mdp.gamma,
                policy0=initial_policy,
                eval_type=1
            )
            pi.setSilent()
            pi.run()
            result = pi.iter
            results.append(result)
        except Exception as e:
            log.error('exception: ' + e.message)
            log.error('won\'t count trial')
        bar.update(t + 1)
    bar.finish()
    if len(results) == 0:
        log.critical('empty results, please check for errors')
        exit(-2)
    results = np.array(results)
    log.info("Value function:")
    log.info(pi.V)
    log.info("Number Iterations:")
    log.info(results)
    log.info('count')
    log.info(len(results))
    log.info('minimum')
    log.info(np.min(results))
    log.info('maximum')
    log.info(np.max(results))
    log.info('mean')
    log.info(np.mean(results))
    log.info('median')
    log.info(np.median(results))
    log.info("")
    return int(np.median(results))


def verify_mdp(mdp):

    log.info('in the verify_mdp function')
    nstates = len(mdp['states'])
    if nstates > 30:
        log.critical('too many states: (' + str(nstates) + ')! seriously?')
        raise Exception('too many states: (' + str(nstates) + ')! seriously?')
    log.debug('legal number of states ' + str(nstates))

    if mdp['gamma'] != 0.75:
        log.critical('Yeah, right. We are going to let that slip... Gamma=' + str(mdp['gamma']) + '!?!?')
        raise Exception('Yeah, right. We are going to let that slip... Gamma=' + str(mdp['gamma']) + '!?!?')

    states = []
    fixed_n_actions = len(mdp['states'][0]['actions'])
    for s in mdp['states']:
        log.debug('state id ' + str(s['id']))

        nactions = len(s['actions'])
        if nactions > 2:
            log.critical('too many actions on a single state: (' + str(nactions) + ')! won\'t do it!')
            raise Exception('too many actions on a single state: (' + str(nactions) + ')! won\'t do it!')
        if fixed_n_actions != nactions:
            log.critical('states should have the same number of actions. Found: (' +
                         str(nactions) + ') and (' + str(fixed_n_actions) + ') clean that up!')
            raise Exception('states should have the same number of actions. Found: (' +
                         str(nactions) + ') and (' + str(fixed_n_actions) + ') clean that up!')

        log.debug('state has correct number of actions ' + str(len(s['actions'])))

        actions = []
        for a in s['actions']:
            log.debug('  action id ' + str(a['id']))

            getcontext().prec = 10
            prob = Decimal(0)
            trans = []
            for t in a['transitions']:

                if not t['probability']:
                    log.critical('transition with zero probability, why would you add that???')
                    raise Exception('transition with zero probability, why would you add that???')

                if t['probability'] < 0:
                    log.critical('negative probability, what am I supposed to do with that???')
                    raise Exception('negative probability, what am I supposed to do with that???')

                if t['probability'] > 1:
                    log.critical('a probability greater than 1?? you should go to Vegas!')
                    raise Exception('a probability greater than 1?? you should go to Vegas!')

                prob += Decimal(t['probability'])
                log.debug('    transition id ' + str(t['id']) + ' with prob ' +
                          str(t['probability']) + ' cumulative prob ' + str(prob))
                trans.append(t)

            if prob != 1.0:
                log.critical('transition probabilities do not equal 1 for a single action, something\'s wrong...')
                raise Exception('transition probabilities do not equal 1 for a single action, something\'s wrong...')
            a['transitions'] = trans
            actions.append(a)

        if s['id'] == 0:
            init_is_terminal = False
            if fixed_n_actions == 1 and s['actions'][0]['transitions'][0]['to'] == 0:
                init_is_terminal = True
            elif s['actions'][0]['transitions'][0]['to'] == 0 and s['actions'][1]['transitions'][0]['to'] == 0:
                init_is_terminal = True

            if init_is_terminal:
                log.critical('Initial state is a terminal state!!! Other states will not be reachable, what?!')
                raise Exception('Initial state is a terminal state!!! Other states will not be reachable, what?!')

        s['actions'] = actions
        states.append(s)

    mdp['states'] = states
    return mdp

def visualize_mdp(mdp, filename):

    log.info('in the visualize_mdp function')
    import pydot
    import networkx as nx
    from networkx.drawing.nx_agraph import write_dot

    G=nx.DiGraph()

    for s in mdp['states']:
        for a in s['actions']:
            for t in a['transitions']:
                ecolor='red' if a['id'] else 'green'
                elabel='p={}, r={}'.format(t['probability'], t['reward'])
                G.add_edge(s['id'], t['to'],
                        color=ecolor,
                        label=elabel)

    log.info('writing dot file')
    write_dot(G, filename.replace('.json', '.dot'))
    g = pydot.graph_from_dot_file(filename.replace('.json', '.dot'))[0]

    log.info('writing png from dot file')
    g.write_png(filename.replace('.json', '.png'))

    log.info('removing intermediate dot file')
    os.remove(filename.replace('.json', '.dot'))
    return filename.replace('.json', '.png')


def main(args):
    """
    """
    log.info('Verbose output enabled ' + str(log.getLogger().getEffectiveLevel()))
    log.debug(args)

    filename = args.mdp_path
    log.info('attempting to load MDP at ' + filename)
    with open(filename) as data_file:
        mdp = json.load(data_file)
    log.debug('file loaded successfully')

    log.info('verifying mdp')
    try:
        mdp = verify_mdp(mdp)
    except:
        log.fatal('MDP has problems. Cannot proceed!')
        exit(-1)

    if args.visualize_mdp:
        log.info('saving json visualization')
        png_path = visualize_mdp(mdp, filename)
        log.info('file found at ' + png_path)

    if args.check_only:
        log.info('mdp was correct and checking only')
        exit(0)

    if args.print_iterations:
        niterations = get_iterations_with_mdptoolbox(mdp)
        log.info('mdp returned median number of iterations ' + str(niterations))
        print('number of iterations: ' + str(niterations))

    log.info('end of script')



if __name__ == '__main__':
    """
    Loads the script and parses the arguments
    """
    from sys import argv
    parser = argparse.ArgumentParser(
        description='Reinforcement Learning and Decision Making, HW3 Tester'
    )
    parser.add_argument(
        '-v',
        help='logging level set to ERROR',
        action='store_const', dest='loglevel', const=log.ERROR,
    )
    parser.add_argument(
        '-vv',
        help='logging level set to INFO',
        action='store_const', dest='loglevel', const=log.INFO,
    )
    parser.add_argument(
        '-vvv',
        help='logging level set to DEBUG',
        action='store_const', dest='loglevel', const=log.DEBUG,
    )

    # json path
    parser.add_argument(
        '-m', '--mdp',
        help='Path to the MDP json file',
        dest='mdp_path', type=str, required=True,
    )
    # verify mdp
    parser.add_argument(
        '-c', '--check_only',
        help='Flag to only check valid MDP on JSON file',
        dest='check_only', action='store_true',
    )
    # iterations
    parser.add_argument(
        '-i', '--iterations',
        help='Calculate how many iterations PI takes to solve this',
        dest='print_iterations', action='store_true',
    )
    # visualize
    parser.add_argument(
        '-s', '--visualize',
        help='Visualize MDP (export to png)',
        dest='visualize_mdp', action='store_true',
    )

    args = parser.parse_args()
    if args.loglevel:
        log.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=args.loglevel)
    else:
        log.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=log.CRITICAL)

    main(args)
