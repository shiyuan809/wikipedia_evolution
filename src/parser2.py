import snap
import numpy as np

def graph_edge_list(page_title, wikilink_link):
    n = len(page_title)
    #print("len page tilte is %d"%n)
    edge_list = {}
    for i in range(n):
        node_1 = page_title[i]

        node_2 = wikilink_link[i]
        if (node_1 not in edge_list):
            edge_list[node_1] = [node_2]
        else:
            edge_list[node_1].append(node_2)

    return edge_list

def graph_snap(page_title, wikilink_link, node_idx_dict):
    graph_snap = snap.TNGraph().New()
    edge_list = graph_edge_list(page_title, wikilink_link)

    for node1 in edge_list:
        node1_idx = node_idx_dict[node1]

        if (not graph_snap.IsNode(node1_idx)):
            graph_snap.AddNode(node1_idx)
        node2_list = edge_list[node1]
  
        
        
        for node2 in node2_list:

            if node2 in node_idx_dict:
                node2_idx = node_idx_dict[node2]
                if (not graph_snap.IsNode(node2_idx)):
                    graph_snap.AddNode(node2_idx)

                if (not graph_snap.IsEdge(node1_idx, node2_idx)):

                    graph_snap.AddEdge(node1_idx, node2_idx)
    return graph_snap

def node_out_degree(page_title, wikilink_link):
    node_out_degree_dict = {}
    edge_list = graph_edge_list(page_title, wikilink_link)
    #print(len(edge_list))
    for node in edge_list:
        node_out_degree_dict[node] = len(edge_list[node])

    return node_out_degree_dict

def node_in_degree(page_title, wikilink_link):
    node_in_degree_dict = {}
    edge_list = graph_edge_list(page_title, wikilink_link)
    for node1 in edge_list:
        node2_list = edge_list[node1]
        for node2 in node2_list:
            if (node2 not in node_in_degree_dict):
                node_in_degree_dict[node2] = 1
            else:
                node_in_degree_dict[node2] += 1

    return node_in_degree_dict


#UNSOLVED: need to use wikilink_is_active filter non-existent nodes
def node_idx_dictionary(page_id, page_title, wikilink_link):
    
    node_idx_dict = {}

    for i in range(len(page_title)):
        if(not(page_title[i] in node_idx_dict.keys())):
            node_idx_dict[page_title[i]] = int(page_id[i])
    j = -2
    for node in wikilink_link:
        if(not(node in node_idx_dict.keys())):
            node_idx_dict[node] = j
            j -=1
    
    return node_idx_dict

def node_num(node_idx_dict):

    return len(node_idx_dict)

def edge_num(page_title):
    return len(page_title)

def processor(addr):
    with open(addr, 'r') as fin:
        feature_list = []
        line_num = 1
        for line in fin:
            line = line.split(',')
            # print('line is : {}'.format(line))
            if (line_num == 1):
                name_list = line
            else:
                feature_list.append(line)
                #print(feature_list)
            line_num += 1
    
    # edge (page_title, wikilink_link)
    # wikilink_is_active : 0 -> node in wikilink_link does not exist in page_title
    #                        1 ->  node in wikilink_link exist in page_title

    #UNSOLVED: this list here has 16 parameters, depending on the format of the dataset, this may or may not work
    [page_id, page_title_old, revision_id, revision_parent_id, revision_timestamp, \
            user_type, user_username, user_id, revision_minor, wikilink_link_old, \
            wikilink_tosection, _ , _, wikilink_section_level, wikilink_section_number, \
            wikinlink_is_active] = zip(*feature_list)


    #RESOLVED: I removed all whitespaces and cast everything to lowercase
    wikilink_link = [None]*len(wikilink_link_old)

    page_title = [None]*len(page_title_old)
    
    for i in range(len(wikilink_link_old)): 
        string = wikilink_link_old[i]
        s = ""
        string = s.join(string.split()).lower()
        wikilink_link[i] = string
    
    for j in range(len(page_title_old)):
        string = page_title_old[j]
        s =""
        string = s.join(string.split()).lower()
        page_title[j] = string

    #UNSOLVED: Need ACTIVE edges and nodes instead!
    node_idx_dict = node_idx_dictionary(page_id, page_title,wikilink_link)

    print('edge_num is : {}'.format(edge_num(page_title)))
    print('node_num is : {}'.format(node_num(node_idx_dict)))
    #print(node_idx_dict)
    print("\n=================")

    
    
    
    #TEST: need node and edges of G to match the numbers printed above!
    
    G = graph_snap(page_title, wikilink_link, node_idx_dict)
    
    print("number of nodes in snap graph is %d"%G.GetNodes())
    print("number of edges in snap graph is %d"%G.GetEdges())
    return G



if __name__ == '__main__':
    processor(addr='enlink_snapshot.2004-03-01.csv')
    #processor(addr='enlink_snapshot.2004-03-01.csv')
