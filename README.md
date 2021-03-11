# Indexation and Ranked Retrieval of Textual Information

[Base Architecture]() | [Memory Concerns]() | [Ranked Retrieval]()

[Code Documentation]() | [Efficiency Metrics]() | [Example Queries]()

## Description

The purpose of this project was to explore the functionality of textual search-engines / information retrieval systems. 
The developed system aims at reading an input text corpus, tokenizing its content, producing an index through approaches that consider memory limitations. Here, the system is capable of accepting relevance feedback to improve the results' precision, with the help of the Rocchio algorithm.
Then a second component provides the implementation of a ranked retrieval method that uses the generated indexes to rapidly answer textual queries.

The execution of the project was divided in 3 stages, each with a corresponding work report:

- The development of a Corpus Reader, a Tokenizer and an Indexer;

- The improvement of the indexation process considering memory limitations;

- The creation of a Ranked Retrieval method to answer queries using generated indexes.

##  Repository Structure

/docs - work reports, diagrams and code documentation

/feedback - feedback provided to the system for improved results (includes pseudo and user feedback)

/input-small - small processed portion of the input data used 

/metrics - metrics used to measure system efficiency

/output-small - sample of the produced indexes

/src - source code

## Instructions 

### Installation

```
cd src
pip3 install -r requirements.txt
```

### Usage Examples

To run the code, please do so inside the src directory. Access the input and the output files by accessing the respective directories.

#### Creating Indexes

An example for the Simple Tokenizer with output going to ../index and various input files located in ../input:

```
python3 CreateIndex.py -o ../index ../input
```

An example for the Simple Tokenizer with limit is(limited by 10000 documents):

```
python3 CreateIndex.py -l 10000 -o ../index ../input
```

An example for the Complex Tokenizer is:

```
python3 CreateIndex.py -t complex -l 100 -o ../index ../input
```

An example for the Complex Tokenizer  and the enabling of the weights calculation is:

```
python3 CreateIndex.py -w -t complex -l 100 -o ../index ../input
```

An example for the Complex Tokenizer  and the enabling of the weights calculation, position storage and memory limitation(500Mb) is:

```
python3 CreateIndex.py -r 0.5 -wp -t complex -l 100 -o ../index ../input
```

#### Querying Indexes

An example using the Simple Tokenizer and a memory limitation of 300Mb, a champions list of size 1000 with output going to ../results, queries located in ../queries.txt and index files in ../input, and returning only the top 10 results:

```
python3 QueryIndex.py -o ../results -t simple -r 0.3 -c 1000 -l 10 ../queries.txt ../input
```

An example using the same configuration but using user feedback considering the top 5 documents retrieved and passing 1, 0.5 and 0.25 as Rocchio's alpha, beta and gamma parameters:

```
python3 QueryIndex.py  -o ../results -t simple -r 0.3 -c 1000 -l 10 -f user -n 5 ../queries.txt ../input 1 0.5 0.25
```

An example using the same configuration as the first but using the Complex Tokenizer, using the pseudo feedback considering the top 20 documents retrieved and passing 1 and 0.5 as Rocchio's alpha and beta parameters:

```
python3 QueryIndex.py -o ../results -r 0.3 -c 1000 -l 10 -f pseudo -n 20 ../queries.txt ../input 1 0.5
```

Auxiliary script where created such as IndexAnalyzer to analyze the resulting indexes, the rocchio auxiliary script to simulate offline user feedback to the system and QueryAnalyzer to calculate the performance metrics of the system.

## Authors

The authors of this repository are Filipe Pires and João Alegria, and the project was developed for the Information Retrieval Course of the Master's degree in Informatics Engineering of the University of Aveiro.

For further information, please read ours reports or contact us at filipesnetopires@ua.pt or joao.p@ua.pt.