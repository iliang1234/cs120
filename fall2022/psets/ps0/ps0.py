#################
#               #
# Problem Set 0 #
#               #
#################


#
# Setup
#
class BinaryTree:
    def __init__(self, root):
        self.root: BTvertex = root
 
class BTvertex:
    def __init__(self, key):
        self.parent: BTvertex = None
        self.left: BTvertex = None
        self.right: BTvertex = None
        self.key: int = key
        self.size: int = None

#
# Problem 1a
#

# Input: BTvertex v, the root of a BinaryTree of size n
# Output: Up to you
# Side effect: sets the size of each vertex n in the
# ... tree rooted at vertex v to the size of that subtree
# Runtime: O(n)
def calculate_sizes(v):
    if v is None:
        return 0

    v.size = 1 + calculate_sizes(v.left) + calculate_sizes(v.right) 
    return v.size

#
# Problem 1c
#

# Input: BTvertex r, the root of a size-augmented BinaryTree T
# ... of size n and height h
# Output: A BTvertex that, if removed from the tree, would result
# ... in disjoint trees that all have at most n/2 vertices
# Runtime: O(h)

half_size = 0
def find_vertex(r): 
    global half_size
    half_size = r.size/2
    
    if r.left is not None:
        left = r.left.size
    else:
        left = 0

    if r.right is not None:
        right = r.right.size
    else:
        right = 0

    if left <= half_size and right <= half_size and ((half_size * 2) - (left + right + 1)) <= half_size:
        return r
    else:
        if left >= right:
            return find_vertex(r.left)
        else:
            return find_vertex(r.right)
        