from colorsys import *

jil = []

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


def getColor(current, threshold):
    val = 60.0 + (float(threshold)-float(current))/float(threshold)*90
    if (val < 0):
        val = 0
    elif (val > 120):
        val = 120
    # print val
    color = list(hsv_to_rgb(val/360., 1, 1))
    for i in range(len(color)):
        color[i] = float(color[i])*255.0
    color = '#%02x%02x%02x' % (color[0], color[1], color[2])
    return color

# print getColor(10,15)


def nodes():

    nodes = []

    for job in jobs:
        d = {}
        d['default'] = "10"
        d['isGroup'] = ""
        for line in job:
            if line.startswith('insert_job'):
                d['key'] = line.split(':')[1].strip()
            if line.startswith('box_name'):
                d['group'] = line.split(':')[1].strip()
            if line.startswith('job_type: box'):
                d['isGroup'] = "true"
                d['text'] = ""
            if line.startswith('time'):
                d['time'] = line.split(':')[1].strip()
                color = getColor(d['time'], d['default'])
                d['color'] = color
            if line.startswith('default'):
                d['default'] = line.split(':')[1].strip()
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
