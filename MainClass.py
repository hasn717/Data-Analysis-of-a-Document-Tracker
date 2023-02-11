import datetime
import json
import os
from collections import Counter, defaultdict
from itertools import groupby
import matplotlib.pyplot as plt
from graphviz import Digraph
from user_agents import parse
from tkinter import messagebox 

import GUI

class MainClass:

    def __init__(self):
        # load the continent and Country codes from json files
        self.continents = self.loadJSON(os.path.join(os.path.dirname(
            __file__), "resources/public_data/", "continent-codes.json"))
        self.countries = self.loadJSON(os.path.join(os.path.dirname(
            __file__), "resources/public_data/", "country-codes.json"))
        self.records = None

    def loadJSON(self, file) -> dict:
        """
        A function that takes a string as input, which specifies JSON file path, and return a list.
        Args:
            file: file path
        Returns:
            Dict containing the data of the parsed JSON file.
        """
       
        data = [json.loads(line) for line in open(file)]
        
        return data
        #print(data)

    def runTasks(self, args: dict):
        task = args['task']
        if args['task'] != '7' and args['task'] is not None:
            self.records = self.loadJSON(args['file_name'])

        if task == '2a':
            docUUID = args['document_uuid']
            result = dict()
           
            for d in self.viewsByCountry(docUUID):
                result[d['Name']] = d['Count']
            if(len(result)==0):
                messagebox.showerror(title="error",message="No data available for this Document uuid")

            else:
            # Histogram of countries of the viewers
                fig, ax1 = plt.subplots(1, 1, figsize=(6, 6))
                fig.suptitle(f'Histogram of Countrie(s) for file:\n{docUUID}')

            # Plot countries
                ax1.bar(result.keys(), result.values())
                ax1.set_title('Countries')
                ax1.set(ylabel='Count')

                plt.show()
            

        elif task == '2b':
            docUUID = args['document_uuid']
            result = dict()
            for d in self.viewsByContinent(docUUID):
                result[d['Name']] = d['Count']
            if(len(result)==0):
                messagebox.showerror(title="error",message="No data available for this Document uuid")
            else:
            # Histogram of continents of the viewers
                fig, ax1 = plt.subplots(1, 1, figsize=(6, 6))
                fig.suptitle(f'Histogram of Continent(s) for file:\n{docUUID}')
            # Plot countries
                ax1.bar(result.keys(), result.values())
                ax1.set_title('Continents')
                ax1.set(ylabel='Count')
                plt.show()

        elif task == '3a':
            result = dict()
            for d in self.viewsByUserAgent():
                result[d['User Agent']] = d['Count']
            # Histogram of continents of the viewers
            fig, ax1 = plt.subplots(1, 1, figsize=(6, 6))
            fig.suptitle('Histogram of User Agents')
            # Plot countries
            ax1.bar(result.keys(), result.values())
            ax1.set_title('User Agents')
            ax1.set(ylabel='Count')
            plt.show()

        elif task == '3b':
            result = dict()
            for d in self.viewsByBrowser():
                result[d['Browser']] = d['Count']
            # Histogram of continents of the viewers
            fig, ax1 = plt.subplots(1, 1, figsize=(6, 6))
            fig.suptitle('Histogram of Browsers')
            # Plot countries
            ax1.bar(result.keys(), result.values())
            ax1.set_title('Browsers')
            ax1.set(ylabel='Count')
            ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)
            plt.show()

        elif task == '4':
            result = dict()
            for d in self.viewTopAvidReaders():
                result[d['visitor_uuid']] = datetime.datetime.fromtimestamp(
                    d['event_readtime'] / 1000).strftime('%H:%M:%S')
            print('Top 10 Readers (Descending)')
            print('visitor_uuid        read time')
            for key, value in result.items():
                print(f'{key}    {value}')

        elif task == '5d':
            if args['sorter'] is None:
                self.viewTopDocuments(
                    args['document_uuid'], args['user_uuid'], sort=None)
            elif args['sorter'] == 'desc':
                self.viewTopDocuments(
                    args['document_uuid'], args['user_uuid'], sort=args['sorter'])

        elif task == '6':
            docUUID = args['document_uuid']
            visUUID = args['user_uuid']
            result = self.viewAlsoLikesDocuments(docUUID, visUUID)
            if(len(result)==0):
                messagebox.showerror(title="error",message="No data available for this Document uuid or user uuid")
            else:
                #print(result)
                value_int = len(self.records)
                value = None
                if value_int >= 1000000:
                    value = "%.0f%s" % (value_int/1000000.00, 'M')
                else:
                    if value_int >= 1000:
                        value = "%.0f%s" % (value_int/1000.0, 'k')

                num = 'Size: ' + value

                graph = Digraph(filename='also_likes.gv')

                graph.node('Readers', color='white')
                graph.node('Documents', color='white')
                graph.edge('Readers', 'Documents', label=num)

                graph.node(docUUID[-4:], style='filled', fillcolor='#3ab125')
                if visUUID is not None and visUUID != "":
                    graph.node(visUUID[-4:], style='filled',
                               fillcolor='#3ab125', shape='box')
                    graph.edge(visUUID[-4:], docUUID[-4:])

                inv_result = {}
                cnt_result = {}
                for k, vs in result.items():
                    for v in vs:
                        inv_result[v] = inv_result.get(v, []) + [k]
                for k, v in inv_result.items():
                    cnt_result[k] = len(v)
                
                for key, values in result.items():
                    for item in values:
                        graph.node(key, shape='box')
                        if item == docUUID[-4:]:
                            graph.node(item, shape='circle')
                        else:
                            graph.node(item, shape='circle', style='filled', fillcolor="/blues3/" + str(cnt_result[item]+1) if max(cnt_result.values()) < 3 else "/blues" + str(max(cnt_result.values())+1) + "/" + str(cnt_result[item]+1))
                        graph.edge(key, item)

                graph.view()

    def viewsByCountry(self, docUUID) -> list:
        """
        A function that take a string as input, which uniquely specifies a document (a document UUID), and return a list of countries of the viewers.
        Args:
            docUUID: document UUID.
        Returns:
            List containing the countries of the viewers.
        """
        result = []
        for x in self.records:
            if x.get('subject_doc_id') == docUUID:
                result.append(x['visitor_country'])
        viewsByCountryList = [{'Code': k, 'Count': v}
                              for k, v in Counter(result).most_common()]
        for d1 in viewsByCountryList:
            for d2 in self.countries:
                if d1['Code'] == d2['Code']:
                    d1.update(d2)

        # print(viewsByCountryList)
        return viewsByCountryList

    def viewsByContinent(self, docUUID) -> list:
        """
        A function that take a string as input, which uniquely specifies a document (a document UUID), and return a list of continents of the viewers.
        Args:
            docUUID: document UUID.
        Returns:
            List containing the continents of the viewers.
        """
        viewsByContinentsList = []
        viewsByCountryList = self.viewsByCountry(docUUID)
        viewsByCountryList = [{k: v for k, v in d.items() if (
            k != 'Code' and k != 'Name')} for d in viewsByCountryList]

        def key(d): return d['Continent']
        viewsByContinentsList = [dict(sum((Counter({k: v for k, v in grp.items() if k != 'Continent'}) for grp in grps), Counter(
        )), Code=Continent) for Continent, grps in groupby(sorted(viewsByCountryList, key=key), key=key)]
        viewsByContinentsList = sorted(
            viewsByContinentsList, key=lambda d: d['Count'], reverse=True)
        for d1 in viewsByContinentsList:
            for d2 in self.continents:
                if d1['Code'] == d2['Code']:
                    d1.update(d2)

        # print(viewsByContinentsList)
        return viewsByContinentsList

    def viewsByUserAgent(self) -> list:
        """
        A function that return a list of all browser identifiers of the viewers.
        Returns:
            List containing all browser identifiers of the viewers.
        """
        result = []
        for x in self.records:
            result.append(x['visitor_useragent'])
        viewsByBrowserList = [{'User Agent': k, 'Count': v}
                              for k, v in Counter(result).most_common()]

        # print(viewsByBrowserList)
        return viewsByBrowserList

    def viewsByBrowser(self) -> list:
        """
        A function that return a list of all browser identifiers of the viewers.
        Returns:
            List containing all browser identifiers of the viewers.
        """
        result = []
        for x in self.records:
            # using Python User Agents to extract Browser family
            result.append(parse(x['visitor_useragent']).browser.family)
        viewsByBrowserList = [{'Browser': k, 'Count': v}
                              for k, v in Counter(result).most_common()]

        # print(viewsByBrowserList)
        return viewsByBrowserList

    def viewTopAvidReaders(self) -> list:
        """
        A function that return a list of the most avid readers.
        Returns:
            List containing Top identifiers of the viewers.
        """
        topAvidReadersList = []
        result = list(
            filter(lambda d: d['event_type'] == 'pagereadtime', self.records))
        result = [{k: v for k, v in d.items() if (
            k == 'visitor_uuid' or k == 'event_readtime')} for d in result]
        # using higher order funcations
        def key(d): return d['visitor_uuid']
        topAvidReadersList = [dict(sum((Counter({k: v for k, v in grp.items() if k != 'visitor_uuid'}) for grp in grps), Counter(
        )), visitor_uuid=visitor_uuid) for visitor_uuid, grps in groupby(sorted(result, key=key), key=key)]
        topAvidReadersList = sorted(
            topAvidReadersList, key=lambda d: d['event_readtime'], reverse=True)[:10]  # only top ten

        # print(topAvidReadersList)
        return topAvidReadersList

    def viewReadersByDocument(self, docUUID) -> list:
        """
        A function that take a string as input, which uniquely specifies a document (a document UUID), and return a list of visitor UUIDs of readers of that document.
        Args:
            docUUID: document UUID.
        Returns:
            List containing the visitor UUIDs of readers of that document.
        """
        readersList = []
        result = list(filter(lambda d: d['event_type'] == 'read' and d['subject_type']
                      == 'doc' and d['subject_doc_id'] == docUUID, self.records))
        readersList = [{k: v for k, v in d.items() if (k == 'visitor_uuid')}
                       for d in result]

        # print(readersList)
        return readersList

    def viewDocumentsByReader(self, visUUID) -> list:
        """
        A function that take a string as input, which uniquely specifies a visitor (a Visitor UUID), and return a list of all documents UUIDs read by the Visitor.
        Args:
            visUUID: Vistor UUID.
        Returns:
            List containing the document UUIDs of read by that visitor.
        """
        documentsList = []
        result = list(filter(lambda d: d['event_type'] == 'read' and d['env_type'] ==
                      'reader' and d['subject_type'] == 'doc' and d['visitor_uuid'] == visUUID, self.records))
        documentsList = [{k: v for k, v in d.items() if (
            k == 'subject_doc_id')} for d in result]

        # print(documentsList)
        return documentsList

    def readersFrequency(self, readers: list, docUUID: str, visUUID=None) -> dict:
        """
        A function to compute frequency of documents.
        Args:
            readers: List of Readers.
            docUUID: document UUID.
            visUUID: Vistor UUID.
        Returns:
            List of documents frequency.
        """
        result = {}
        for reader in readers:
            if visUUID is not None and reader['visitor_uuid'] == visUUID:
                continue
            documents = self.viewDocumentsByReader(reader['visitor_uuid'])

            for document in documents:
                if document['subject_doc_id'] != docUUID:
                    if document['subject_doc_id'] not in result:
                        result[document['subject_doc_id']] = 1
                    else:
                        result[document['subject_doc_id']] += 1

        # print(result)
        return result

    def viewTopDocuments(self, docUUID, visUUID:  str = None, sort: str = None) -> list:
        """
        A function that take a string as input, which uniquely specifies a document (a document UUID), optionaly visitor (a Visitor UUID),  and optionaly sort; and return a list of top documents.
        Args:
            docUUID: document UUID.
            visUUID: Vistor UUID.
            sort: Sorter.
        Returns:
            List containing the top documents UUIDs and readers count.
        """
        readers = self.viewReadersByDocument(docUUID)
        if(len(readers)==0):
            messagebox.showerror(title="error",message="No data available for this Document uuid ")

        else:
            if sort is None:
                sortType = '(Alphabetical (ASC) on Document UUID)'
                records = self.readersFrequency(readers, docUUID, visUUID)
                sortedDict = dict(sorted(records.items())[:10])
            else:
                sortType = '(Descending on Count of Readers)'
                records = self.readersFrequency(readers, docUUID, visUUID)
                sortedDict = dict(
                    sorted(records.items(), key=lambda item: item[1], reverse=True)[:10])

            print('Top 10 Documents ' + sortType)
            print('Document UUID                                    # Readers')
            for key, value in sortedDict.items():
                print(f'{key}    {value}')

        # print(sortedDict)
            return sortedDict

    def viewAlsoLikesDocuments(self, docUUID, visUUID:  str = None) -> list:
        """
        A function to generate “also like” functionality.
        Args:
            docUUID: document UUID.
            visUUID: Vistor UUID.
        Returns:
            List containing the top documents UUIDs and readers count.
        """
        # Using default dictionary to provide a default value for the key that does not exists.
        result = defaultdict(list)
        readers = self.viewReadersByDocument(docUUID)
        for reader in readers:
            if visUUID is None:
                for d in self.viewDocumentsByReader(reader['visitor_uuid']):
                    result[reader['visitor_uuid'][-4:]
                           ].append(d['subject_doc_id'][-4:])
            elif visUUID is not None and reader['visitor_uuid'][-4:] != visUUID[-4:]:
                for d in self.viewDocumentsByReader(reader['visitor_uuid']):
                    result[reader['visitor_uuid'][-4:]
                           ].append(d['subject_doc_id'][-4:])

        # print(result)
        return result
