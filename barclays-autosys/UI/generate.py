from colorsys import *

jil = []

nodes = [] 
start_time = 130.
with open('../Machine Description.txt', 'rb') as file:
    for row in file:
        if (not row.startswith('#')):
            jil.append(row.strip())

    jobs = []
    job_indices = []

    for i in range(len(jil)):
        if (jil[i].startswith('insert_job')):
            job_indices.append(i)
    # jobs = []
    for i in range(len(job_indices) - 1):
        jobs.append(jil[job_indices[i]:job_indices[i + 1]])

    jobs.append(jil[job_indices[len(job_indices)-1]:])


def getColor(current, threshold, status):
    val = 60.0 + (float(threshold)-float(current))/float(threshold)*90
    if (val < 0):
        val = 0
    elif (val > 120):
        val = 120
    # print val
    sat = 1.0
    if status == "incomplete":
        sat = 0.5
    color = list(hsv_to_rgb(val/360., sat, 1))
    for i in range(len(color)):
        color[i] = float(color[i])*255.0
    color = '#%02x%02x%02x' % (color[0], color[1], color[2])
    return color

# print getColor(10,15)


def get_nodes():
    global nodes
    nodes = []

    for job in jobs:
        d = {}
        d['default'] = "10"
        d['isGroup'] = ""
        d['status'] = "incomplete"
        d['group'] = ""
        d['time'] = 0.
        # d['default'] = 0.
        for line in job:
            if line.startswith('insert_job'):
                d['key'] = line.split(':')[1].strip()
            if line.startswith('box_name'):
                d['group'] = line.split(':')[1].strip()
            if line.startswith('status'):
                d['status'] = line.split(':')[1].strip()
            if line.startswith('job_type: box'):
                d['isGroup'] = "true"
                d['text'] = ""
            if line.startswith('time'):
                d['time'] = line.split(':')[1].strip()
                color = getColor(d['time'], d['default'], d['status'])
                d['color'] = color
            if line.startswith('default'):
                d['default'] = line.split(':')[1].strip()
            if line.startswith('cum'):
                d['cum'] = line.split(":")[1].strip()
        if (not d['isGroup'] == "true"):
            d['text'] = d['key']
            # del d['isGroup']

        
        nodes.append(d)

    for node in nodes:
        if (node['isGroup'] == "true"):
            node['time'] = 0.0
            node['default'] = 0.0
            # print node
            for node2 in nodes:
                if (not node2['isGroup'] == "true"):
                    if node2['group'] == node['key']:
                        node['default'] += float(node2['default'])
                        node['time'] += float(node2['time'])

    for node in nodes:
        for node2 in nodes:
            if (node2['isGroup'] == "true" and node2['group'] == node['key']):
                node['default'] += float(node2['default'])
                node['time'] += float(node2['time'])



    return nodes

def box_info():
    pass
    
# nodes()

def links():
    links = []

    for job in jobs:
        d = {}
        name = ""
        for line in job:
            
            if line.startswith('insert_job'):
                name = line.split(':')[1].strip()
            if line.startswith('condition'):
                d['to'] = name
                d['from'] = line.split('(')[1].split(')')[0]
        if (not d == {}):
            links.append(d)
           

    return links


def time_details():
    global nodes, start_time
    # print nodes
    # start_time = 200. # This is in minutes
    duration = 0.
    target = 0.
    for node in nodes:
        if (not node['isGroup'] == "true"):
            duration += float(node['time'])
            target += float(node['default'])

    end_time_target = start_time + target
    end_time_pred = start_time + duration
    start_time_copy = "%i:%i" % (int(start_time/60), int(start_time%60))
    end_time_pred_copy = "%i:%i" % (int(end_time_pred/60), int(end_time_pred%60))
    end_time_target_copy = "%i:%i" % (int(end_time_target/60), int(end_time_target%60))

    return {"end_time_pred": end_time_pred_copy, "end_time_target": end_time_target_copy, "start_time": start_time_copy}

# a = get_nodes()
# print time_details()