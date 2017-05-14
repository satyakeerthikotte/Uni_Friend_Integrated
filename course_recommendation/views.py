from django.shortcuts import render, get_object_or_404
from.models import jobs,courses,services
from django.db.models import Count
from django.http import JsonResponse
# from rest_framework import viewsets
import re
import logging, logging.config
import sys

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

logging.config.dictConfig(LOGGING)


def index(request):
    return render(request, 'uni_friend-frontend/index.html')

def job(request):
    all_j = jobs.objects.all()
    jobs_count=jobs.objects.count()
    domainNames=jobs.objects.values('domain').distinct()
    domainNamesCounts=jobs.objects.values('domain').annotate(domainCount=Count('domain'))

    # test=jobs.objects.values('location').distinct()
    state=""
    uniqueStates=[]
    uniStatesCount=[]
    pos=0
    sCount=0
    for job in all_j:
        state=str([job.location]).split(',')[1]
        # print(state[:3])
        if state[:3] not in uniqueStates:
            uniqueStates.append(state[:3])
            uniStatesCount.append([state[:3],1])
        else:
            pos=uniqueStates.index(state[:3])
            sCount=uniStatesCount[pos][1]
            uniStatesCount[pos]=([state[:3],sCount+1])

    print (uniqueStates)
    print(uniStatesCount)

    # print(test.query)
    # print (test.split(','))
    return render(request, 'uni_friend-frontend/courserec.html',{'all_jobs': all_j, 'jobs_count':jobs_count, 'domain_names_count':domainNamesCounts,'statesJobCount':uniStatesCount})



def jobSelStates(request,state):
    selStateJobs = jobs.objects.filter(location__contains=state)
    # print selStateJobs
    # return render(request, 'uni_friend-frontend/googleMapDiv.html', {'all_jobs': selStateJobs})
    return render(request, 'uni_friend-frontend/courserec.html',{'all_jobs': selStateJobs})

def recommend(request,job_id,prog=None):
    rec_courses = []
    recommend_courses=[]
    dict={}
    jobfull = get_object_or_404(jobs,pk=job_id)
    jobdesc = jobfull.description.lower()
    job_list = re.split("[^a-zA-Z0-9]", jobdesc)
    keywrods={

        'CMPE 225':['java','python'],
        'CMPE 280':['html','css','css3','jquery','node','full', 'stack'],
        'CMPE  124': ['logic design', 'digital logic', 'switching circuits', 'digital systems', 'digital circuits',
                      'design of systems', 'digital computers', 'control systems', 'data communications', 'electronic',
                      'digital hardware', 'logic gates', 'combinational logic', 'registers', 'counters', 'memory unit',
                      'asynchronous sequential logic', 'digital integrated circuits', 'laboratory experiments'],
        'CMPE  126': ['algorithms', 'data structure', 'c', 'c++', 'programming', 'languages', 'software', 'analysis',
                      'object oriented', 'data analyst', 'data scientist'],
        'CMPE  142': ['linux', 'windows', 'unix', 'kernel architecture', 'command line interfaces', 'gui', 'threads',
                      'context switching', 'concurrent processing', 'parallel processing', 'semaphores',
                      'multiprocessor', 'multithreaded architectures', 'processes', 'threads', 'concurrency issues',
                      'locks', 'mutexes', ' monitors'],
        'CMPE  206': ['basic networking', 'networks', 'protocols', 'network layers', 'osi model', 'tcp/ip', 'ip',
                      'network design', 'routing', 'network topology', 'physical layer', 'data link layer',
                      'network layer', 'transport layer', 'session layer', 'presentation layer', 'application layer',
                      'ethernet', 'extranet', 'routers', 'switches', 'modems', 'bridges', 'repeaters', 'hubs',
                      'network interface'],
        'CMPE 207': ['tcp', 'ip', 'ssl','networking software', 'bsd sockets', 'winsock', 'procedure call', 'sockets',
                     'connection oriented', 'connectionless', 'client', 'servers', 'client server communication',
                     'command line', 'tcp', 'udp', 'mutex lock', 'semaphores', 'deadlock'],
        'CMPE 208': ['protocols of network', 'transport layer protocols', 'application layer protocols',
                     'network architecture', 'protocols', 'wireshark', 'packet analyser', 'subnetting', 'subnet mask',
                     'packets', 'tcp/ip packets', 'paload', 'packet size', 'http', 'dns', 'ospf', 'arp', 'ipv4', 'ipv6',
                     'nat', 'dhcp', 'icmp', 'igmp', 'ccna'],
        'CMPE 209': ['network security', 'network protocols', 'network applications', 'cryptography algorithms',
                     'authentication systems', 'intrusion detection', 'network attacks', 'network defenses',
                     'system level security issues', 'encryption', 'decryption', 'man in middle attack',
                     'security architecture', 'network infrastucture', 'cyber security'],
        'CMPE 210': ['sdn', 'network function', 'nfv', 'open source', 'virtualization', 'openvswitch',
                     'software defined networking', 'floodlight', 'open source controller', 'opendaylight', 'helium',
                     'nfs', 'vim', 'infrastructure', 'virtual'],
        'CMPE 239': ['data mining', 'web mining', 'data preprocessing', 'association rules', 'sequential patterns',
                     'data classification', 'data clustering', 'web crawling', 'information retrieval',
                     'search engines', 'social network analysis', 'link analysis', 'web usage mining',
                     'web personalization', 'recommender systems'],
        'CMPE 226': ['mysql','php','xml','database architecture', 'database technologies', 'enterprise systems', 'structured data',
                     'semi-structured data', 'unstructured data', 'relational database', 'non-relational database',
                     'sql', 'data warehouse', 'data lake', 'etl', 'rdbms', 'data', 'data query', 'data modelling',
                     'database design', 'data retrieval', 'data indexing', 'tables'],
        'SE 188': ['machine learning', 'pattern recognition', 'big data analytics', 'big data',
                   'machine learning theories', 'machine learning approaches', 'machine learning algorithms',
                   'supervised learning', 'unsupervised learning', 'learning theory', 'data analysis',
                   'collaborative filtering', 'social network', 'data analysis techniques', 'recommendation system'],
        'CMPE 272': ['enterprise software', 'enterprise software development', 'oss', 'noss', 'sql', 'databases',
                     'tp monitors', 'groupware', 'java platform', 'distributed objects', 'component technologies',
                     'distributed systems management', 'conceptual model', 'software technologies'],
        'CMPE 273': ['application protocols', 'distributed systems', 'object request brokers', 'asynchronous messaging',
                     'web services', 'java programming', 'cap theorem', 'python', 'go', 'concurrency pattern',
                     'enterprise messaging', 'rpc', 'integration protocol', 'remote procedure call', 'restful',
                     'web services', 'consistency model', 'fault tolerance', 'application security'],
        'CMPE 277': ['smartphone application', 'android', 'smartphone', 'activity', 'mvc', 'intents', 'fragments',
                     'action bar','menu bar', 'looper', 'handler', 'threads', 'processes', 'ui design','security','ios',
                     'google api','android   architecture','programming concepts','deployment environment'],
        'CMPE 281': ['cloud computing', 'cloud','cloud architectures','cloud infrastructure','enterprise adoption',
                     'software-as-a-service', 'saas','platform-as-a-service', 'paas',
                     'infrastructure-as-a-service', 'iaas',
                     'data center', 'cloud computing',
                     'openstack', 'devops', 'jenkins',
                     'gradle', 'cloud application',
                     'big data', 'hadoop', 'nosql',
                     'web technologies', 'cloud security',
                     'virtualization', 'amazon aws', 'aws',
                     'data storage'],
        'CMPE 202': ['software design',
                     'software development',
                     'system design',
                     'design methodologies',
                     'software modeling',
                     'software architecture',
                     'uml diagrams',
                     'use cases templates',
                     'crc cards',
                     'class diagrams',
                     'sequence diagrams',
                     'activity diagrams',
                     'software methodologies',
                     'uml heuristics',
                     'open source',
                     'software analysis',
                     'pattern languages',
                     'anti patterns'],
        'CMPE 275': [
            'enterprise application architecture',
            'enterprise',
            'spring framework',
            'google guice',
            'aspect oriented programming',
            'mvc',
            'data persistence',
            'transaction management',
            'application security',
            'java messaging service',
            'google appengine'],
        'EE 281': [
            'network design',
            'tcp/ip',
            'stack architecture',
            'osi model',
            'data delivery',
            'ip',
            'atm',
            'ip addressing',
            'datagram routing',
            'performance evaluation',
            'congestion control',
            'routing protocol',
            'encoding',
            'tunneling',
            'subnetting',
            'icmp',
            'arp',
            'rarp',
            'ip protocol',
            'igp',
            'cidr',
            'udp',
            'sliding window'],
        'EE 284': [
            'convergence of voice',
            'data networks',
            'packet network',
            'internet protocol',
            'networked multimedia',
            'voice over ip',
            'voip',
            'ip protocols',
            'deployment',
            'multimedia network',
            'sctp',
            'ip networking'],
        'EE 289': [
            'networking protocols',
            'network technologies',
            'mobile',
            'wireless network',
            'lte',
            'wifi',
            'bluetooth',
            'network architectures',
            'mobile networking',
            'wireless scenarios',
            'cellular',
            'fog networks',
            'internet'],
        'EE 283': [
            'virtualization concepts',
            'components',
            'infrastructure',
            'hardware virtualization',
            'software virtualization',
            'virtualization machine',
            'life cycle management',
            'virtualization services'],
        'CMPE 220': [
            'system software',
            'assemblers',
            'macro-assemblers',
            'loaders and linkers',
            'compilers',
            'operating systems',
            'compiler function',
            'loader function',
            'assembler design',
            'embedded software',
            'operating system',
            'yacc'],
        'CMPE 236': [
            'mobile web system',
            'mobile architectures',
            'mobile security',
            'mobile design',
            'mobile platforms',
            'mobile cloud',
            'database',
            'access services'],
        'CS 251a': [
            'software activities',
            'object oriented',
            'artifacts',
            'software development',
            'UML',
            'domain data',
            'workflows',
            'system requirements',
            'deployment',
            'java',
            'linux',
            'domain modelling'],
        'CS 251b': [
            'design artifacts',
            'design phase',
            'object oriented',
            'software development',
            'design metrics',
            'design patterns',
            'refactoring',
            'frameworks',
            'testing'],
        'CS 265': [
            'Security mechanisms',
            'protecting',
            'networks',
            'cryptography',
            'security services',
            'distributed systems',
            'access control',
            'protection models',
            'security policies',
            'secure systems',
            'firewalls',
            'design',
            'intrusion detection',
            'detection',
            'encryption',
            'decryption',
            'network security',
            'security',
            'authentication',
            'symmetric key',
            'public key',
            'hash functions',
            'authorization',
            'software flaws',
            'malware'],
        'CS 235': [
            'interaction',
            'direct manipulation',
            'interfaces',
            'websites',
            'website collections',
            'testing',
            'metaphors',
            'visualization',
            'agile development',
            'design pattern',
            'navigational models',
            'ui',
            'user interface',
            'graphic designer',
            'iterative design',
            'page layout',
            'ui design',
            'conceptual model',
            'uxability'],
        'CS 218': [
            'cloud computing',
            'distributed system',
            'virtual machines',
            'virtualization',
            'cloud platform architectures',
            'IaaS',
            'PaaS',
            'SaaS',
            'service oriented architecture',
            'cloud programming',
            'software environments',
            'peer to peer computing',
            'ubiquitous cloud',
            'cloud security',
            'trust management',
            'containers',
            'iot',
            'mobile',
            'big data',
            'computing',
            'cloudlets',
            'resource',
            'paradigms',
            'parallel systems',
            'storage systems',
            'security',
            'privacy',
            'fog computing',
            'edge computing'],
        'CS 274': [
            'xml',
            'DTD',
            'Schema',
            'Namespace',
            'XSLT',
            'XPath',
            'Xquery',
            'Encryption',
            'RDF',
            'RDFS',
            'Ontology',
            'web services',
            'data conversion',
            'Semantic web application',
            'recommendation system',
            'link analysis',
            'data mining'],
        'CS 160': [
            'Software engineering principles',
            'software process',
            'process models',
            'software analysis',
            'software design',
            'configuration management',
            'quality control',
            'project planning',
            'ethical issues',
            'software development',
            'design documentation',
            'design',
            'command line',
            'sql',
            'linux',
            'java',
            'c',
            'c++',
            'perl',
            'python',
            'fork',
            'pipes',
            'apache',
            'testing',
            'implementation',
            'software life cycles'],
        'CS 146': [
            'data structure',
            'algorithm',
            'tree structures',
            'priority queues',
            'heaps',
            'directed graphs',
            'undirected graphs',
            'radix sort',
            'heapsort',
            'mergesort',
            'quicksort',
            'data structures',
            'Divide and conquer',
            'greedy',
            'dynamic programming',
            'algorithm design'],
        'CS 257': [
            'Design management',
            'file organization',
            'data access',
            'buffer management',
            'storage management',
            'Query processing',
            'query optimization',
            'transaction management',
            'data recovery',
            'data concurrency control',
            'data protection'],
        'CS 258': [
            'network',
            'Internet technologies',
            'TCP/IP',
            'network media',
            'software defined networks',
            'sdn',
            'networks supporting',
            'cloud computing',
            'network security',
            'peer to peer',
            'quality of services',
            'network virtualization',
            'sdn',
            'openflow',
            'openflow switches',
            'controllers',
            'iot',
            'internet of things',
            'data center',
            'ethernet',
            'lan virtualization',
            'security'],
        'CS 259': [
            'hardware architecture',
            'software development',
            'multi-threaded',
            'parallel processing',
            'algorithms',
            'parallel hardware architectures',
            'parallel programming',
            'GPU processing',
            'computer gaming',
            'clusters',
            'pthreads',
            'cuda',
            'opencl',
            'mpi',
            'openmp',
            'hadoop',
            'grids',
            'clouds',
            'parallelism',
            'multi-core',
            'microprocessor'],
    }
    a_list=keywrods.keys()
    for i in job_list:
        for course_num in a_list:
            if(i in keywrods.get(course_num)):
                rec_courses.append(course_num)
    fil_courses = set(rec_courses)
    for k in fil_courses:
        count = rec_courses.count(k)
        dict[k] = count


    if prog is None:
        for l in range(len(dict)):
            if (dict.values()[l]) >= 2:
                recommend_courses.append(courses.objects.filter(number=dict.keys()[l]))
    else:
        for l in range(len(dict)):
            if (dict.values()[l]) >= 2:
                recommend_courses.append(courses.objects.filter(number=dict.keys()[l],program=prog ))


    # return JsonResponse(data)

    return  render(request, 'uni_friend-frontend/modelPopUp.html',{'jobs': jobfull ,'filter_courses': recommend_courses })


def navServices(request):
    return render(request,'uni_friend-frontend/sjsunav.html')

def servicesInfo(request):
    all_services = services.objects.order_by('name')
    # print(all_services)
    return render(request, 'uni_friend-frontend/servinfo.html', {'services': all_services})