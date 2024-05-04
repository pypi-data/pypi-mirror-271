import os
import argparse
from ete3 import Tree


replace_clade_usage = '''
======================= replace_clade example commands =======================

TreeSAK replace_clade -m main.tree -s sub.tree -l leaves.txt -o output.tree

==============================================================================
'''


def replace_clade(main_tree_file, sub_tree_file, tree_out):

    # read in sub tree
    sub_tre = Tree(sub_tree_file, format=1)

    # get all leaves in sub tree
    subtree_leaf_name_list = sub_tre.get_leaf_names()

    # read in main tree
    main_tre = Tree(main_tree_file)

    # remove clades
    lca = main_tre.get_common_ancestor(subtree_leaf_name_list)

    if len(lca.get_leaf_names()) != len(subtree_leaf_name_list):
        print('LCA of subtree leaves in main tree contain extra leaves, program exited!')
        exit()

    lca_p = lca.up
    lca_p.remove_child(lca)
    lca_p.add_child(sub_tre)

    # write out updated tree
    main_tre.write(outfile=tree_out, format=8)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-m',   required=True,  help='main file')
    parser.add_argument('-s',   required=True,  help='sub file')
    parser.add_argument('-l',   required=True,  help='main tree leaves')
    parser.add_argument('-o',   required=True,  help='output tree')
    args = vars(parser.parse_args())
    replace_clade(args)
