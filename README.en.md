# CS61A 2024

中文版：[README.md](README.md)

This repository contains my answers to the CS61A assignments, labs, and projects for future reference. The original Chinese comments are preserved, with English translations directly below them. They include detailed reasoning, brief notes, and questions I had at the time. The links below point to selected problem-solving notes:

- [HW04: Maximum path sum in a tree](hw/AChw04/hw04.py#L165-L166): an attempted way to compare branches.
- [HW05: A path containing a target value](hw/AChw05/hw05.py#L82-L96): how each recursive result is extended with the current node.
- [HW06: Notes on classes](hw/AChw06/hw06.py#L12-L13) and [the linked-list problem](hw/AChw06/hw06.py#L109-L182): impressions from implementing a class, first encountering Link, and questions about nested first values.
- [HW09: Building a list in a Scheme macro](hw/AChw09/hw09.scm#L13-L23): the relationship between map, cons, and the cond clauses.
- [Lab08: Pruning and removing from a tree](lab/AClab08/lab08.py#L58-L69): confusion and attempts involving remove and recursive pruning.
- [Lab12: Shared exam rooms in SQL](lab/AClab12/lab12.sql#L36-L37): selecting rooms shared by different courses.
- [Hog: A dice-rolling turn](proj/AChog/hog.py#L44-L45): why all required rolls are completed even after a 1 appears.
- [Cats: Edit distance](proj/ACcats/cats.py#L233-L547): a long explanation of the move from recursion to dynamic programming, including states, initialization, transitions, and complexity.
- [Scheme: Evaluation and special forms](proj/ACScheme/scheme_eval_apply.py#L23-L87), [argument handling for define](proj/ACScheme/scheme_forms.py#L43-L44), and [notes on a confusing part](proj/ACScheme/scheme_forms.py#L220-L221): thoughts and questions about evaluation, environment lookup, and argument structure.

## Repository cleanup

The repository was previously archived. During the course, I uploaded the course framework, testing tools, and static assets along with my answers. This cleanup keeps my answers and problem-solving notes while removing runtime files I no longer need. The repository remains, but is not intended to be a runnable course environment. I reset the Git history because old commits may have retained local paths or other personal information.
