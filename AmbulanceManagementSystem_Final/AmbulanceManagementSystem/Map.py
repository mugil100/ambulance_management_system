import folium as mp
import osmnx as ox

osm_file_path = r"data/map.osm"  
G = ox.graph_from_xml(osm_file_path, bidirectional=False)

class Map:
    def __init__(self, map_center=[10.661692943004194, 77.00608909852019], z_start=16):
        self.mapobj = mp.Map(location=map_center, zoom_start=z_start, zoom_control=True)
        
        mp.TileLayer(tiles='openstreetmap', name='openstreetmap', control=True, show=True).add_to(self.mapobj)
        mp.TileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
                     name='CartoDB.DarkMatter', attr="CartoDB.DarkMatter", control=True, show=False).add_to(self.mapobj)
        mp.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}.png',
                     name='Esri.WorldStreetMap', attr="Esri.WorldStreetMap", control=True, show=False).add_to(self.mapobj)
        
        self.Lay_hos_obj = mp.FeatureGroup(name="Hospital").add_to(self.mapobj)
        self.Lay_amb_obj = mp.FeatureGroup(name="Ambulance").add_to(self.mapobj)
        self.Lay_pat_obj = mp.FeatureGroup(name="Patient").add_to(self.mapobj)
        self.Lay_path_amb_obj = mp.FeatureGroup(name="Shortest path to Patient From Ambulance Station").add_to(self.mapobj)
        self.Lay_path_hos_obj = mp.FeatureGroup(name="Shortest path to HospitalFrom Patient").add_to(self.mapobj)
        
        self.bounds_coordinates = [[10.6645224, 77.0082095], [10.6708229, 77.0208333], 
                                   [10.6536419, 77.0047728], [10.6537968, 77.0210230]]

    def layers(self):
        hospitals = [
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
        
        ambulance_stations = [
           {"coordinates":[10.6600, 77.0050],"name":"A"},
           {"coordinates":[10.66327, 77.01779],"name":"B"},
           {"coordinates":[10.6670, 77.0125],"name":"C"},
           {"coordinates":[10.6685, 77.0070],"name":"D"},
           {"coordinates":[10.6555, 77.0100],"name":"E"},
           {"coordinates":[10.6615, 77.0070],"name":"F"},
       ]
        for hospital in hospitals:
            strhos = f"<h3><center>{hospital['name']}</center></h3><center><img src='data/hospital.jpg' alt='Hospital' width='100' height='60'></center>"
            mp.Marker(
                location=hospital["coordinates"],
                icon=mp.Icon(color='red', icon='plus-sign'),
                popup=mp.Popup(strhos, max_width=300)
            ).add_to(self.Lay_hos_obj)
        
        for station in ambulance_stations:
            stramb = f"<h3><center>{station['name']}</center></h3><center><img src='data/ambulance.jpg' alt='Ambulance' width='100' height='60'></center>"
            mp.Marker(
                location=station["coordinates"], 
                icon=mp.Icon(icon='star', color='darkblue'),
                popup=mp.Popup(stramb, max_width=300)  
            ).add_to(self.Lay_amb_obj)

    def plot(self, loc, opt,relate,pt_details,pid):
        if relate!="Stranger" : 
            strpat = f"<h3><center>{pt_details}</center></h3><center><h4><center>Patient ID :{pid}</center></h4><h5>{opt}</h5></center><center><img src='data/patient.jpg' alt='Patient' width='100' height='60'></center>"
            mp.Marker(
                location=loc,
                icon=mp.Icon(color='green', icon='user'),
                popup=mp.Popup(strpat, max_width=300)
            ).add_to(self.Lay_pat_obj)
        else:
            strpat = f"<h4><center>Patient ID :{pid}</h4></center><h5><center>{opt}</center></h5><center><img src='data/patient.jpg' alt='Patient' width='100' height='60'></center>"
            mp.Marker(
                location=loc,
                icon=mp.Icon(color='green', icon='user'),
                popup=mp.Popup(strpat, max_width=300)
            ).add_to(self.Lay_pat_obj)

    def createmap(self,loc,opt,relate,pt_details,pid):
        self.layers()
        self.plot(loc, opt,relate,pt_details,pid)
        self.layers()
        self.mapobj.fit_bounds(self.bounds_coordinates)

    def plot_path_am(self,path,loc,end_loc,opt,relate,pt_details,pid):
        pc = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in path]
        pc.insert(0, loc)  
        pc.append(end_loc)
        mp.PolyLine(locations=pc, color='red', weight=5).add_to(self.Lay_path_amb_obj)
        self.createmap(loc,opt,relate,pt_details,pid)
        
    def plot_path_hs(self,path,loc,end_loc,opt,relate,pt_details,pid):
        pc = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in path]
        pc.insert(0, loc)  
        pc.append(end_loc)
        mp.PolyLine(locations=pc, color='blue', weight=5).add_to(self.Lay_path_hos_obj)
        self.createmap(loc,opt,relate,pt_details,pid)
    
    def layercontrol(self):
        mp.LayerControl().add_to(self.mapobj)
    
    def show(self):
        self.mapobj.save("Map.html")

mop = Map()

def ploth(path,loc,end_loc,opt,relate,pt_details,pid):
    mop.plot_path_hs(path,loc,end_loc,opt,relate,pt_details,pid)
def plota(path,loc,end_loc,opt,relate,pt_details,pid):
    mop.plot_path_am(path,loc,end_loc,opt,relate,pt_details,pid)    
def show():
    mop.show()
def LayerControl():
    mop.layercontrol()
    
