import osmnx as ox
import heapq
import GUI as gp
import Map as Map
import time 
import Cramers_Analysis as cr
import Administrator_gui as ad
import Res_GUI as gpi
def main():
    class Data:
        def __init__(self):
            self.hospitals = [
                {"coordinates": [10.659502, 77.000567], "name": "SN Hospital"},
                {"coordinates": [10.659480, 77.000535], "name": "JP Hospital"},
                {"coordinates": [10.658091, 77.009836], "name": "Government Head Quarters Hospital"},
                {"coordinates": [10.662770, 76.999580], "name": "Mcv Memorial Ent Trust Hospital"},
                {"coordinates": [10.657625, 77.011446], "name": "Pkd Nursing Home"},
                {"coordinates": [10.662422, 77.003040], "name": "AVM Hospital"},
                {"coordinates": [10.662538, 77.003431], "name": "K.M Hospital"},
                {"coordinates": [10.664762, 77.004966], "name": "MRS Hospital & Fertility centre"},
                {"coordinates": [10.665069, 77.005867], "name": "Thirumalai Hospital"},
                {"coordinates": [10.668211, 77.007036], "name": "Arathana Hospital"},
                {"coordinates": [10.670235, 77.007422], "name": "KGM HOSPITAL"},
                {"coordinates": [10.662683, 77.009689], "name": "Prabhu Hospital"},
                {"coordinates": [10.662994, 77.010016], "name": "Kowsalya Medical Centre"},
                {"coordinates": [10.662933, 77.010601], "name": "Sakthi Hospital"},
                {"coordinates": [10.662759, 77.012280], "name": "Surya Hospital"},
                {"coordinates": [10.662295, 77.012529], "name": "Ar Ortho Hospital"},   
                {"coordinates": [10.662549, 77.012991], "name": "Arun Hospital - Multi-Speciality Hospital"},
                {"coordinates": [10.663202, 77.015002], "name": "Shanthi Hospital"},
                {"coordinates": [10.663307, 77.010094], "name": "Siva Meds Multispeciality Hospital"},
                {"coordinates": [10.664198, 77.010357], "name": "Pills Hospital"},
                {"coordinates": [10.674253, 77.008098], "name": "The Pollachi Cardiac Center"}
            ]
                
            self.ambulance_stations = [
                {"coordinates":[10.6600, 77.0050],"name":"A"},
                {"coordinates":[10.66327, 77.01779],"name":"B"},
                {"coordinates":[10.6670, 77.0125],"name":"C"},
                {"coordinates":[10.6685, 77.0070],"name":"D"},
                {"coordinates":[10.6555, 77.0100],"name":"E"},
                {"coordinates":[10.6615, 77.0080],"name":"F"},
            ]
    
    class ShortestPath:
        def __init__(self):
            pass
        
        def dijkstra_unidirection(self, adj_list, start, end):
            distances = {node: float("inf") for node in adj_list}
            distances[start] = 0
            priority_queue = [(0, start)]
            previous_nodes = {node: None for node in adj_list}
        
            while priority_queue:
                current_distance, current_node = heapq.heappop(priority_queue)
                if current_distance > distances[current_node]:
                    continue
                for neighbor, weight in adj_list[current_node]:
                    distance = current_distance + weight
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous_nodes[neighbor] = current_node
                        heapq.heappush(priority_queue, (distance, neighbor))
                        
            path = []
            current = end
            while current is not None:
                path.insert(0, current)
                current = previous_nodes[current]
            
            return path, distances[end] if distances[end] != float("inf") else None
        
        def dijkstra_bidirection(self, adj_list, start, end):
            forward_distances = {node: float("inf") for node in adj_list}
            backward_distances = {node: float("inf") for node in adj_list}
            forward_distances[start] = 0
            backward_distances[end] = 0
    
            forward_queue = [(0, start)]
            backward_queue = [(0, end)]
            
            forward_previous = {node: None for node in adj_list}
            backward_previous = {node: None for node in adj_list}
    
            visited_forward = set()
            visited_backward = set()
            
            shortest_path = float("inf")
            meeting_node = None
    
            while forward_queue and backward_queue:
                forward_distance, forward_node = heapq.heappop(forward_queue)
                backward_distance, backward_node = heapq.heappop(backward_queue)
                
                if forward_node in visited_backward or backward_node in visited_forward:
                    meeting_node = forward_node if forward_node in visited_backward else backward_node
                    break
    
                if forward_distance <= forward_distances[forward_node]:
                    visited_forward.add(forward_node)
                    for neighbor, weight in adj_list[forward_node]:
                        distance = forward_distance + weight
                        if distance < forward_distances[neighbor]:
                            forward_distances[neighbor] = distance
                            forward_previous[neighbor] = forward_node
                            heapq.heappush(forward_queue, (distance, neighbor))
                
                if backward_distance <= backward_distances[backward_node]:
                    visited_backward.add(backward_node)
                    for neighbor, weight in adj_list[backward_node]:
                        distance = backward_distance + weight
                        if distance < backward_distances[neighbor]:
                            backward_distances[neighbor] = distance
                            backward_previous[neighbor] = backward_node
                            heapq.heappush(backward_queue, (distance, neighbor))
    
            if meeting_node:
                path = []
                current = meeting_node
                while current is not None:
                    path.insert(0, current)
                    current = forward_previous[current]
                
                current = backward_previous[meeting_node]
                while current is not None:
                    path.append(current)
                    current = backward_previous[current]
                
                shortest_path = forward_distances[meeting_node] + backward_distances[meeting_node]
                return path, shortest_path
    
            return None, None
        
        def dijkstra_multidirectional(self, adj_list, starts, ends):
            distances = {node: float("inf") for node in adj_list}
            priority_queue = []
            previous_nodes = {node: None for node in adj_list}
    
            for start in starts:
                distances[start] = 0
                heapq.heappush(priority_queue, (0, start))
            
            visited = set()
            shortest_path = float("inf")
            meeting_node = None
    
            while priority_queue:
                current_distance, current_node = heapq.heappop(priority_queue)
                if current_node in ends:
                    shortest_path = current_distance
                    meeting_node = current_node
                    break
                if current_node in visited:
                    continue
                visited.add(current_node)
                for neighbor, weight in adj_list[current_node]:
                    distance = current_distance + weight
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous_nodes[neighbor] = current_node
                        heapq.heappush(priority_queue, (distance, neighbor))
            if meeting_node:
                path = []
                current = meeting_node
                while current is not None:
                    path.insert(0, current)
                    current = previous_nodes[current]
                return path, shortest_path
            return None, None
    
    
    def build_adjacency_list(G):
        adj_list = {}
        for u, v, data in G.edges(data=True):
            weight = data.get('length', 1)
            if u not in adj_list:
                adj_list[u] = []
            if v not in adj_list:
                adj_list[v] = []
            adj_list[u].append((v, weight))
            adj_list[v].append((u, weight))
        return adj_list
    
    osm_file_path = r"data/map.osm"
    G = ox.graph_from_xml(osm_file_path, bidirectional=True)
    adj_list = build_adjacency_list(G)
    
    pid,relate, pt_name, pt_gender, start_lat, start_long, opt = gp.get_details()
    start_lat, start_long = float(start_lat), float(start_long)
    pt_details = f"<p style='line-height: 0.5;'><center>{pt_name}</center><br><center>{pt_gender}</center></p>"
    start_node = ox.distance.nearest_nodes(G, X=start_long, Y=start_lat)
    
    def find_nearest_location(data_list, start_node, adj_list, algo_type):
        shortest_distance = float("inf")
        best_path, best_location_name, best_end_coords = None, "", None
        sp = ShortestPath()
    
        for location in data_list:
            end_lat, end_long = location["coordinates"]
            end_node = ox.distance.nearest_nodes(G, X=end_long, Y=end_lat)
            
            if algo_type == 1:
                path, distance = sp.dijkstra_unidirection(adj_list, start_node, end_node)
            elif algo_type == 2:
                path, distance = sp.dijkstra_bidirection(adj_list, start_node, end_node)
            elif algo_type == 3:
                path, distance = sp.dijkstra_multidirectional(adj_list, [start_node], [end_node])
            else:
                continue
            
            if distance and distance < shortest_distance:
                shortest_distance = distance
                best_path = path
                best_location_name = location["name"]
                best_end_coords = (end_lat, end_long)
        
        return best_location_name, shortest_distance, best_path, best_end_coords
    
    data = Data()
    hospital_name, distance_h, path_h, end_location_h = [""] * 3, [0.0] * 3, [None] * 3, [None] * 3
    station_name, distance_a, path_a, end_location_a = [""] * 3, [0.0] * 3, [None] * 3, [None] * 3
    time_c = [0.0] * 3
    
    for i in range(3):
        st = time.time()
        hospital_name[i], distance_h[i], path_h[i], end_location_h[i] = find_nearest_location(data.hospitals, start_node, adj_list, i + 1)
        time_c[i] = time.time() - st
        st = time.time()
        station_name[i], distance_a[i], path_a[i], end_location_a[i] = find_nearest_location(data.ambulance_stations, start_node, adj_list, i + 1)
        time_c[i] += time.time() - st
    
    h_index = distance_h.index(min(distance_h))
    h_name, dist_h, ph_h, end_h = hospital_name[h_index], distance_h[h_index], path_h[h_index], end_location_h[h_index]
    
    a_index = distance_a.index(min(distance_a))
    a_name, dist_a, ph_a, end_a = station_name[a_index], distance_a[a_index], path_a[a_index], end_location_a[a_index]
    
    dist_a=dist_a/1000
    dist_h=dist_h/1000
    
    if ph_h:
        Map.ploth(ph_h, (start_lat, start_long), end_h, opt, relate, pt_details,pid)
    if ph_a:
        Map.plota(ph_a, (start_lat, start_long), end_a, opt, relate, pt_details,pid)
    
    algorithm = ["Dijkstra Unidirection", "Dijkstra Bidirection", "Dijkstra Multidirectional"]
    for i in range(3):
        print(f"{algorithm[i]:25s} -> Time Taken: {time_c[i]:0.4f}")
    
    value=cr.main(time_c)
    
    Map.LayerControl()
    
    gpi.GUI(h_name,dist_h,a_name,dist_a)
    
    if (input("Nedded to Acess Administrator Page :")in "YESyes"):
        username="Administrator"
        password="123456"
            
        username1=input(" Enter The User Name : ")
        password1=input(" Enter The Password  : ")
    
        if(username==username1):
            if(password==password1):
                ad.gui(value)
def map_show():
    Map.show()


   



