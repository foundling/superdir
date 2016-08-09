import os
import utils
import pdb

class Tree:

    def __init__(self, indent_size=None, output_dir=None):

        if os.path.exists(output_dir):
            raise IOError('The directory {} already exists'.format(self.output_dir))

        self.indent_size = indent_size
        self.output_dir = output_dir
        self.abs_base_path = None
        self.data = None
        self.root = None

    def build_tree(self):
        ''' Derive parent/child hierarchy from current and previous lines' indentation relationship.  '''

        virtual_root = self._make_new_node(
            parent=None,
            value='virtual_root',
            children=[]
        )
        root = self._make_new_node(
            parent=virtual_root,
            value=self.output_dir, 
            children=[]
        )
        virtual_root['children'].append(root)

        parent_node = virtual_root
        indent = -1
        for line in self.data:

            new_indent = utils.get_indent(line, self.indent_size)

            if new_indent > indent:
                parent_node = parent_node['children'][-1]

            elif new_indent < indent:
                distance = indent - new_indent
                parent_node = self._find_ancestor(parent_node, distance)

            child = self._make_new_node(
                parent   = parent_node, 
                value    = utils.get_dirname(line) if utils.is_dir(line) else utils.get_filename(line), 
                children = [] if utils.is_dir(line) else None
            ) 

            parent_node['children'].append(child)
            indent = new_indent

        self.root = virtual_root

    def walk(self, callback):
        ''' Walk tree and call callback on each node. '''
        
        def _walk(tree, path=self.abs_base_path):

            for node in tree['children']:

                callback(node, level=level)

                if node['children'] is not None:
                    _walk(node, path)

        tree = self.root
        _walk(tree)

    def load_data(self, data):
        ''' Load the input data and clean it. '''

        self.data = utils.clean(data)

    def _set_paths(self):
        '''
        ABSOLUTE:

            original output_dir = /data/apps/new_app 

            full_base_path = /data/apps
            output_dir = new_app 

        RELATIVE WITH MULTIPLE LEVELS:

            original output_dir = apps/new_app 

            full_base_path = cwd() + '/' + apps/
            output_dir = new_app 

        RELATIVE WITH A SINGLE LEVEL:

            original_output_dir = new_app

            full_base_path = cwd() 
            output_dir = new_app 
        '''
        pass

    def _make_new_node(self, parent=None, value=None, children=None):
        ''' create a new node. if children is Nonetype, node is treated as a leaf. '''
        return  dict(parent=parent, value=value, children=children)

    def _find_ancestor(self, start_node, parents_to_visit):
        ''' use indentation level relative to previous line to find ancestor.'''
        current_node = start_node

        while (parents_to_visit > 0):
            current_node = current_node['parent']
            parents_to_visit -= 1

        return current_node
