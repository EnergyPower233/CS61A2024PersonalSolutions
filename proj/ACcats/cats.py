"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########

#Accpeted
def pick(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns True. If there are fewer than K such paragraphs, return
    the empty string.

    Arguments:
        paragraphs: a list of strings
        select: a function that returns True for paragraphs that can be selected
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    cnt = 0
    for x in paragraphs:
        if select(x):
           if cnt == k:
               return x
           cnt += 1
    return '' 
    # END PROBLEM 1

#Accepted
def about(subject):
    """Return a select function that returns whether
    a paragraph contains one of the words in SUBJECT.

    Arguments:
        subject: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in subject]), 'subjects should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def check(string):
        for x in subject:
            for y in split(lower(remove_punctuation(string))):
                if x == y:
                    return True
        return False
    return check
    # END PROBLEM 2

#Accepted
def accuracy(typed, source):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of SOURCE that was typed.

    Arguments:
        typed: a string that may contain typos
        source: a string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)
    source_words = split(source)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    if not (typed_words + source_words):
        return 100.0
    if (len(source_words) == 0 and len(typed_words) != 0) or (len(typed_words) == 0 and len(source_words) != 0):
        return 0.0
    Correct = 0
    # for i, j in zip(typed_words, source_words):
        # Correct += 1 if i == j else 0
    Correct = sum(i == j for i, j in zip(typed_words, source_words))
    return Correct / len(typed_words) * 100
    # END PROBLEM 3

#Accepted
def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return len(typed) / 5 / elapsed * 60
    # END PROBLEM 4


############
# Phase 2A #
############

#Accepted
def autocorrect(typed_word, word_list, diff_function, limit):
    """Returns the element of WORD_LIST that has the smallest difference
    from TYPED_WORD. If multiple words are tied for the smallest difference,
    return the one that appears closest to the front of WORD_LIST. If the
    difference is greater than LIMIT, instead return TYPED_WORD.

    Arguments:
        typed_word: a string representing a word that may contain typos
        word_list: a list of strings representing source words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    res = ''
    cnt = 1e9
    if typed_word in word_list:
        return typed_word
    else:
        for x in word_list:
            current_diff = diff_function(typed_word, x, limit)
            if current_diff < cnt:
                cnt = current_diff
                res = x
        return res if cnt <= limit else typed_word
    # END PROBLEM 5

#Accepted, Anwser Checked 
def feline_fixes(typed, source, limit):
    """A diff function for autocorrect that determines how many letters
    in TYPED need to be substituted to create SOURCE, then adds the difference in
    their lengths and returns the result.

    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> feline_fixes("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> feline_fixes("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> feline_fixes("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> feline_fixes("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> feline_fixes("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    # assert False, 'Remove this line'
    def f(typed, source, times):
        if times > limit:
            return times
        if len(typed) == 0 or len(source) == 0:
            return abs(len(typed) - len(source))
        elif typed[0] == source[0]:
            return f(typed[1:], source[1:], times)
        else:
            return f(typed[1:], source[1:], times + 1) + 1
    return f(typed, source, 0)  
        
    # END PROBLEM 6


############
# Phase 2B #
############

#Hard, Accepted, Anwser Checked, Algorithm: DP

def minimum_mewtations(typed, source, limit):
    """A diff function that computes the edit distance from TYPED to SOURCE.
    This function takes in a string TYPED, a string SOURCE, and a number LIMIT.
    Arguments:
        typed: a starting word
        source: a string representing a desired goal word
        limit: a number representing an upper bound on the number of edits
    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)      # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """
    # if typed in source:
        #  abs(len() - )
    # assert False, 'Remove this line'
    
    
    #Official Solution, Provided by GPT-5
    # 按Ctrl + / 是全部注释
    # Press Ctrl + / to toggle comments for all selected lines.
    
    # if limit < 0: # Base cases should go here, you may add more base cases as needed.
    #     # BEGIN
    #     "*** YOUR CODE HERE ***"
    #     return limit + 1
    #     # END
    # if typed == source: # do nothing if typed and source are equal
    #     return 0
    
    # #if any list are empty, return length( whose value represents the times need to add or delete)
    # if len(typed) == 0: 
    #     return min(len(source), limit + 1)
    # if len(source) == 0:
    #     return min(len(typed), limit + 1)
    # # Recursive cases should go below here
    
    # if typed[0] == source[0]: # Feel free to remove or add additional cases
    #     # BEGIN
    #     "*** YOUR CODE HERE ***"
    #     return minimum_mewtations(typed[1:], source[1:], limit) #do nothing if letters are equal
    #     # END
    # else:
    #     # Fill in these lines
    #     add = 1 + minimum_mewtations(typed, source[1:], limit - 1)
    #     #if you add a letter, which means current letter (being checked) in the source is linked with the letter you added
    #     #so forfeit(skip?) the current letter
    #     remove = 1 + minimum_mewtations(typed[1:], source, limit - 1)
    #     #same as add, removing a letter from typed and adding a letter to source have same effects
    #     substitute = 1 + minimum_mewtations(typed[1:], source[1:], limit - 1)
    #     #just ignore this letter and ++limit
    #     # BEGIN
    #     "*** YOUR CODE HERE ***"
    #     return min(add, remove, substitute) 
    #     # END


    #Source / Inspiration : LeetCode72: Edit-Distance
    #https://leetcode.com/problems/edit-distance/description/
    #Dynamic Programming, Provided by shuo-liu 16
    #DP 即 Dynamic Programming 动态规划
    # DP means dynamic programming.
    #太棒了 学了3小时 我逐渐理解一切
    # Great, after studying for three hours, I'm starting to understand everything.
    #下面注释全是我写的 GPT说胡话 让我来讲
    # I wrote all the comments below. GPT was talking nonsense, so let me explain it.
    #脑子乱 先不用英语了
    # My thoughts are all over the place; I'll stop using English for now.
    #m 行 n 列
    # m rows, n columns.
    #i 行 j 列
    # Row i, column j.
    m, n = len(typed) + 1, len(source) + 1
    dp = [[0] * (n) for i in range(m)]
    #构建 m * n的矩阵 全部初始化为0 为什么长度是len+1? 因为要多开一行空的 这个放倒后面解释
    # Build an m * n matrix and initialize every entry to 0. Why is each dimension len + 1? We need one extra row and column for the empty string; I'll explain that below.
    #dp 的每一个格子 保存的是 当前的情况下 所需要做的最少的修改次数
    # Each cell in dp stores the minimum number of edits needed for the current case.
    #比如 dp[i][j] 就是取 typed 的前 i 个字母和 source 的前 j 个字母 组成的字符串
    # For example, dp[i][j] represents the prefixes made from the first i letters of typed and the first j letters of source.
    #在这种情况下 我们想把 typed的前i个字母 变成 source 的 前 j 个字母 所需要做的操作次数
    # In this case, we want to turn the first i letters of typed into the first j letters of source; this is the number of operations required.
    
    for i in range(1, m):
        dp[i][0] = i
    for j in range(1, n):
        dp[0][j] = j
    #这是在把第一行填满
    # This fills the first row.
    #我们就用 horse行 和 ros列 举例子吧
    # Let's use horse for the row and ros for the columns as an example.
    #第一行开的全部都是0 相当于ros我们一个字母都不取 现在列是空的
    # The first row is all zeros: for ros, we take no letters, so the column is empty.
    #我们想要把horse变成ros的前0个字母(空的) 就是有多少个字母就删除多少个字母
    # We want to turn horse into the first zero letters of ros (the empty string), so we delete every letter.
    #比如hor 想要变成空 我就要 把h o r 三个字母全部删掉 那我的操作次数就是三
    # For example, to turn hor into the empty string, I delete h, o, and r; that takes three operations.
    #竖着依然是同理的
    # The vertical direction works the same way.
#       # h o r s e
#     # 0 1 2 3 4 5 
#     r 1
#     o 2
#     s 3
    #为什么要初始化为这个样子?
    # Why initialize it this way?
    #这就是DP的特性了
    # That's the idea behind DP.
    #我们注意到 想要获得 horse 变成 ros 的结果 实际上只要获得这三个的结果,然后取最小的就可以了:
    # Notice that to find the result of turning horse into ros, we only need the results of these three cases, then choose the minimum:
    #这个例子来自https://leetcode.cn/problems/edit-distance/solutions/188223/bian-ji-ju-chi-by-leetcode-solution/
    # This example comes from https://leetcode.cn/problems/edit-distance/solutions/188223/bian-ji-ju-chi-by-leetcode-solution/.
    # 1 hors 变成 ro 的过程 (只要删除一个字母 horse就可以变成hors 从而变成 ros)
    # 1. The process of turning hors into ro (delete one letter: horse becomes hors, then turn it into ros).
    # 2 horse 变成 ro 的过程 (可以同过增加一个字母ro --> ros 来获得 ros)
    # 2. The process of turning horse into ro (add one letter, ro --> ros, to get ros).
    # 3 hors 变成 ros 的过程 (只要删除一个字母 horse 就可以变成 hors 从而变成 ros)
    # 3. The process of turning hors into ros (delete one letter: horse becomes hors, then turn it into ros).
    #实际上 这对于任何一步都是成立的 每一个格子都是这样的
    # This holds at every step; every cell follows the same pattern.
    #但是如果字母相等 我们就没必要考虑它了 那一步操作是不需要的 他们自然就相等了
    # If the letters match, there is no need to consider an operation; they already match.
    #于是我们可以这样写出来我们的状态转移方程:
    # So we can write the state-transition equation as follows:
    #dp[i][j] = dp[i - 1][j - 1] if type[i - 1] == source[j - 1] else 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    #type[i - 1] == source[j - 1] 说明两个字母相等 字符串也是数组 只不过每个数是个char
    # typed[i - 1] == source[j - 1] means the two letters match. A string is also an array, with each element being a char.
    # [] 里面是下标 因为我们的dp相较于字符串的长度多开了1行和1列表示空 所以我们必须给dp的下标减1才是字符串所对应的字母
    # The values in [] are indices. Since dp has one extra row and column for the empty string, subtract one from a dp index to get the corresponding character in the string.
    #别忘了dp是保存的操作次数 相等就是不用操作 不相等要么增删要么替换 都算作一次操作
    # Remember, dp stores the number of operations. Matching letters require no operation; otherwise, an insertion, deletion, or replacement each counts as one.
    #根据我们的矩阵表 我们首先要锁定字母相等的时候:
    # Looking at the matrix, first handle the case where the letters match:
#       # h o r s e
#     # 0 1 2 3 4 5 
#     r 1     *
#     o 2   *
#     s 3       *
    #这个时候这个位置的值是等于它的左上角的dp[i - 1][j - 1]的
    # At this point, the value in this cell equals its upper-left neighbor, dp[i - 1][j - 1].
    #而其他字母不相等的时候呢 我们就需要它上边左边和左上角最小的一个值 再加 1 操作次数
    # When the letters do not match, take the minimum of the values above, to the left, and upper-left, then add one operation.
    #还是不要忘了我们dp的这个格子存储的是当前的操作次数
    # Again, remember that each dp cell stores the current number of operations.
    #我们先把第二行和第二列填出来:
    # Let's fill in the second row and second column first:
#       # h o r s e
#     # 0 1 2 3 4 5 
#     r 1 1 2 2 3 4 # d[3][1]这个位置r相等了 所以不需要操作哦 直接从左上角d[2][0]转移
# At d[3][1], the r's match, so no operation is needed; copy the value from the upper-left cell, d[2][0].
#     o 2 2         # 根据直觉也是对的 hor 转成 r 只用删掉ho嘛
# This also matches intuition: to turn hor into r, just delete ho.
#     s 3 3
    #知道怎么回事了 我们把剩下的填出来
    # Now I get it; let's fill in the rest.
#       # h o r s e
#     # 0 1 2 3 4 5 
#     r 1 1 2 2 3 4 
#     o 2 2 1 2 3 4
#     s 3 3 2 2 2 3
#     于是我们便得到了d[5][3] == 3
# So we get d[5][3] == 3.
#     所以horse 变成 ros只需要三次操作: 把h换r rorse 删除第二个r和e ros
# It takes only three operations to turn horse into ros: replace h with r to get rorse, then delete the second r and e to get ros.
    #我们来看看每个点是怎么填出来的:
    # Let's see how each cell is filled:
#       #   h   o   r   s   e
#     # 0   1   2   3   4   5
#        X   X   !
#         X   X   !
#          X   X   !*
#     r 1   1   2  *2*XX3XXX4
#        X   !      *X
#         X   !       X
#          X   !*      X
#     o 2   2  *1*XX2   3XXX4
#        X      *X   !
#         X     X X   !
#          X    X  X   !*
#     s 3   3   2   2  *2*XX3
#                       *

#   我猜你已经理解一切了
# I think you've got it now.
#   我们只需要顺序把它填好 然后返回dp[m - 1][n - 1]就可以了 (括号里是下标, 所以要 - 1)
# We just fill the table in order, then return dp[m - 1][n - 1] (the indices are zero-based, hence the - 1).
    for i in range(1, m):# 0那行在初始化的时候已经填过了 所以我们从1开始
    # The first row was already initialized, so we start at 1.
        for j in range(1, n):
            #为什么以一行一行的填的顺序填呢
            # Why fill the table row by row?
            #其实一列一列地填也可以 只要保证你填写的过程里每一个格子在填写之前都知道它的左上角,左边和上面的格子的值就可以了
            # It can also be filled column by column, as long as every cell's upper-left, left, and upper neighbors have values before that cell is filled.
            dp[i][j] = dp[i - 1][j - 1] if typed[i - 1] == source[j - 1] else 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
            #这是那个状态转移方程 还记得吧
            # Remember, this is the state-transition equation.
    #然后直接return最右下角的格子的值就好了
    # Then just return the value in the bottom-right cell.
    #这个过程全程没有用到递归 你所需要的值其实全部都在上一步算过了 还存了起来
    # This process uses no recursion. Everything we need was computed and stored in earlier steps.
    #所以这个是要比答案快的 答案有好多次重复访问 递归深度比较高
    # This is faster than the provided solution, which revisits many states and has a greater recursion depth.
    return dp[m - 1][n - 1]
    #可是这个想要得到答案就必须算完 在算完之前是永远不知道它和limit相比到底是多了还是少了的
    # However, to get the answer, we have to finish the whole table. Until then, we cannot know whether the result exceeds limit.
    #所以我们也没有用到limit 因为算出来的值如果超limit了 题目只要求返回比limit大的任意一个值就可以了
    # So we do not use limit: if the result exceeds it, the problem only requires returning any value greater than limit.
    
    #我们讲万事万物都有个根 为什么这题能想到用动态规划呢
    # Every idea has a root. How can we tell that this problem can be solved with dynamic programming?
    #只要看https://oi-wiki.org/dp/
    # Just look at https://oi-wiki.org/dp/.
    #那么其实你已经知道了 dp[i][j]就是 状态 那个三目运算就是 状态转移方程
    # Then you already know: dp[i][j] is the state, and the ternary expression is the state-transition equation.
    #三个条件: 最优子结构，无后效性和子问题重叠
    # The three conditions are optimal substructure, no aftereffect, and overlapping subproblems.
    #1  最优子结构: horse 转成 ros 的 最优解 是通过其他三个的最优解 的 最小的那一个 来 转移 的 
    # 1. Optimal substructure: the optimal way to turn horse into ros is derived from the minimum of the optimal results of the other three cases.
    #   而其中每一个格子的最优解都是通过这样的方法来转移
    # Each cell's optimal result is derived in the same way.
    #   那么这个问题所拆解的子问题的最优解 和这个问题的最优解 它的方案是一样的
    # So the optimal solutions to the subproblems and the solution to the original problem follow the same rule.
    #   也就是说 这个方案的子问题的最优解 是这个问题的最优解(实现)的过程中的一部分
    # In other words, each optimal subproblem solution is part of the process of constructing the optimal solution to the original problem.
    #   那如果它的子问题不是最优解呢?
    # What if a subproblem's solution is not optimal?
    #   如果子问题不是最优解 我们可以将这个子问题的这个解更换为它的最优解 于是把这个更换为最优解的子问题作为原问题的子问题的解
    # If a subproblem's solution is not optimal, we can replace it with its optimal solution and use that as the subproblem result for the original problem.
    #   此时原问题的解会比原来的更优 所以原来的解就不是最优解 矛盾了
    # Then the original solution would be better than before, which contradicts the claim that the old solution was optimal.
    #   那么要使它这个问题的解是最优解 它的子问题就必然是最优解
    # Therefore, for the solution to this problem to be optimal, its subproblem solutions must also be optimal.
    #2  无后效性: 这是必然的 因为每一个格子的值并不取决于它的子问题的格子是怎么被走到的 我们只需要知道它的子问题的格子的值就好了
    # 2. No aftereffect: each cell's value does not depend on the path taken to reach its subproblem cell; we only need that cell's value.
    #附上GPT给出的详细定义:
    # Here is the detailed definition GPT gave:
    # 说“这道题满足无后效性”，其实就是在说一句很朴素的话：
    # Saying that a problem has no aftereffect is just a plain way of saying:
    # 我现在这个子问题的最优解，只取决于我这个子问题本身的状态（i、j），不取决于我是怎么走到这里的。
    # The optimal solution to this subproblem depends only on its own state (i, j), not on how we got here.
    # 放到你这道编辑距离里，就是：
    # For this edit-distance problem, that means:
    # 子问题：把 typed 的前 i 个字符变成 source 的前 j 个字符，最少要几步
    # Subproblem: turn the first i characters of typed into the first j characters of source in the fewest steps.
    # 记成：dp[i][j]
    # We write it as dp[i][j].
    # 无后效性要检查的就是：我在算 dp[i][j] 的时候，是不是只需要前面已经算好的那几个状态就行了，还是说我还得知道“之前是先删再插，还是先插再删”这种历史？
    # To check for no aftereffect, when computing dp[i][j], do we only need the states already computed, or must we also know whether we deleted before inserting or inserted before deleting?
    # 答案是：不用知道历史，只要知道那几个子问题的值就行。所以它满足无后效性。
    # The answer is that we do not need the history; we only need those subproblem values. So it has no aftereffect.
    # 有“后效”的情况一般是这种：
    # A problem with an aftereffect often looks like this:
    # 我现在在状态 (i, j)，但我需要知道我之前是怎么删/怎么插的，因为不同路径会影响我后面的选择。
    # I am at state (i, j), but I need to know how I deleted or inserted before, because different paths may affect my next choices.
    # 比如有些问题会说“连续删三个会便宜一点”或者“重复操作会有折扣”，那就会导致：你光知道现在删了多少个字符还不够，你还得知道这几个是不是连续的。那就是有后效，需要把“历史”也编码进状态。
    # For example, if three consecutive deletions are cheaper or repeated operations get a discount, knowing only how many characters have been deleted is not enough; we also need to know whether those deletions were consecutive. That is an aftereffect, so history must be encoded in the state.
    # 但这道题的三种操作（插入、删除、替换）每一步的成本都是 1，而且彼此独立，不会说“你前面删过，就不能再插”“你前面替换过，这次替换变便宜了”这种事，所以历史对未来没有影响——只看现在的长度位置就行。
    # But here each of the three operations (insert, delete, replace) costs 1, independently. Deleting earlier does not prevent an insertion, and a previous replacement does not make the next one cheaper. History does not affect the future; only the current positions matter.
    # 有后效性就是：你在某个状态下要做决策时，仅仅知道这个状态本身的信息还不够，你还必须知道这个状态是怎么被走到/转移到这里的，因为不同的到达方式会影响接下来能做的选择或这些选择的代价。
    # An aftereffect means the state information alone is not enough to make a decision. We also need to know how we reached or transitioned to this state, because different paths can affect the next choices or their costs.
    # 换句话说：
    # In other words:
    # 同一个“表面上看起来一样的状态”，因为历史不同，后面的最优结果也会不同；
    # The same apparent state can lead to different optimal results because of different histories;
    # 所以这个“表面状态”不能唯一决定后续，要把历史信息也一起塞进状态里，否则就会算错。
    # so the apparent state alone does not determine what comes next. History must also be included in the state, or the result may be wrong.
    #3 子问题重叠
    # 3. Overlapping subproblems.
    #和答案的递归相比你就发现了DP的好处了
    # Compared with the recursive solution, this is where you see the benefit of DP.
    #其实我们算的东西它的思路是一样的 但是答案使用函数递归出来算的 我们注意每推进一步 它总是要算 它add substitute remove 的递归的值
    # The idea is the same, but the provided solution uses recursion. At every step it recursively computes the add, substitute, and remove cases.
    #其实有些值它之前已经算过了 可是算完之后因为函数出了frame return完了之后立马就销毁了
    # Some values may already have been computed, but when a function frame returns, those values are immediately discarded.
    #它真的重复地算了好多好多遍
    # It really recomputes the same things over and over.
    #比如 substitute = 1 + minimum_mewtations(typed[1:], source[1:], limit - 1)
    # For example:
    #就是状态转移的过程 它递归之后本质上还是由它的下一步的 add remove substitute来决定的
    # This is the state-transition process. After recursion, each step is still determined by the next add, remove, and substitute cases.
    #这导致了什么 我们要把深度开到它递归到由else前面的内容终止掉 才能一步一步往上传值 这是很费劲的
    # As a result, recursion has to go all the way down until one of the conditions before else stops it, then pass results back up step by step. That is cumbersome.
    #你就类比之前我举例的爬楼梯 你想要第10个台阶 就得要第九个和第八个
    # Think of the staircase example I mentioned earlier: to reach the 10th step, you need the 9th and 8th.
    #你从1一直加到10算的快还是从10要到1算的快
    # Is it faster to count from 1 to 10, or start at 10 and work back to 1?
    #这个也是一样的
    # It is the same here.
    #DP的时间复杂度是O(n^2) for里有个for嘛 这是显然的
    # DP takes O(n^2) time because there are two nested for loops; that is obvious.
    #官方的解法就十分甚至九分的幽默了(wzr说开memorize 他简直就是memorize魔怔人)
    # The official solution is pretty funny, to say the least (wzr says to use memoization; they are completely fixated on it).
    #它每次要往回传3个情况 所以是O(3^n)  (虽然答案看代码还是挺优雅的 但是还是笑嘻了)
    # It returns three cases at every step, so it takes O(3^n) time (the solution code looks elegant, but it still makes me laugh).
    #可是当如果我们想给官方的解法实现memorize的时候 它的实现方式就是DP()
    # If we tried to add memoization to the official solution, its implementation would just become DP.
    #当然也可以开一个memo的字典 用ij坐标表示key 该点的最优解是value
    # Of course, we could make a memo dictionary using (i, j) as the key and the best result for that cell as the value.
    #可是你都知道有坐标这种东西了为什么不直接DP呢(((((
    # But if we already have coordinates, why not just use DP?(((((
        
        
    #加了memo的是这样的:(Provided By GPT)
    # This is what it looks like with memoization (provided by GPT):
    # memo = {}

    # def helper(i, j):
    #     # i 表示 typed 用到了下标 i 之后的部分 -> typed[i:]
    # i means that the remaining part of typed starts at index i: typed[i:].
    #     # j 表示 source 用到了下标 j 之后的部分 -> source[j:]
    # j means that the remaining part of source starts at index j: source[j:].
    #     if (i, j) in memo:
    #         return memo[(i, j)]

    #     # 有一边空了，另一边剩多少就得做多少步
    # If one side is empty, the number of steps is the length of the other side.
    #     if i == len(typed):
    #         return len(source) - j
    #     if j == len(source):
    #         return len(typed) - i

    #     # 当前字符一样，就都往后走，不加步数
    # If the current characters match, advance both without adding a step.
    #     if typed[i] == source[j]:
    #         ans = helper(i + 1, j + 1)
    #     else:
    #         # 三种操作
    # The three operations.
    #         add_cost = 1 + helper(i, j + 1)      # 在 typed 里加上 source[j]
    # Add source[j] to typed.
    #         remove_cost = 1 + helper(i + 1, j)   # 删掉 typed[i]
    # Delete typed[i].
    #         sub_cost = 1 + helper(i + 1, j + 1)  # 把 typed[i] 换成 source[j]
    # Replace typed[i] with source[j].
    #         ans = min(add_cost, remove_cost, sub_cost)

    #     memo[(i, j)] = ans
    #     return ans

    # return helper(0, 0)

    
    
    
def final_diff(typed, source, limit):
    """A diff function that takes in a string TYPED, a string SOURCE, and a number LIMIT.
    If you implement this function, it will be used."""
    # assert False, 'Remove this line to use your final_diff function.'
FINAL_DIFF_LIMIT = 6 # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########

#Accepted
def report_progress(typed, source, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        typed: a list of the words typed so far
        source: a list of the words in the typing source
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> typed = ['how', 'are', 'you']
    >>> source = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(typed, source, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], source, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    res = 0
    for i in range(len(typed)):
        if typed[i] != source[i]:
            res = i
            break
        else:
            res = i + 1
    prog = res / len(source)
    upload({'id': user_id, 'progress': prog})
    return prog
    # END PROBLEM 8

#Accpeted
def time_per_word(words, timestamps_per_player):
    """Given timing data, return a match data abstraction, which contains a
    list of words and the amount of time each player took to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        timestamps_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> match = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> get_all_words(match)
    ['collar', 'plush', 'blush', 'repute']
    >>> get_all_times(match)
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    res = []
    for i in timestamps_per_player:
        times = []
        for j in range(len(i) - 1):
            times.append(i[j + 1] - i[j])
        res.append(times)
    return match(words, res)
    # END PROBLEM 9


def fastest_words(match):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        match: a match data abstraction as returned by time_per_word.

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words(match(['Just', 'have', 'fun'], [p0, p1]))
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    player_indices = range(len(get_all_times(match)))  # contains an *index* for each player
    word_indices = range(len(get_all_words(match)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    res = []
    for i in range(len(player_indices)): 
        res.append([])
    for i in word_indices:
        itr = 0
        for j in player_indices:
            if time(match, j, i) < time(match, itr, i):
                itr = j
        res[itr].append(get_word(match, i))
    return res
        
        
    # END PROBLEM 10


def match(words, times):
    """A data abstraction containing all words typed and their times.

    Arguments:
        words: A list of strings, each string representing a word typed.
        times: A list of lists for how long it took for each player to type
            each word.
            times[i][j] = time it took for player i to type words[j].

    Example input:
        words: ['Hello', 'world']
        times: [[5, 1], [4, 2]]
    """
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return {"words": words, "times": times}


def get_word(match, word_index):
    """A utility function that gets the word with index word_index"""
    assert 0 <= word_index < len(get_all_words(match)), "word_index out of range of words"
    return get_all_words(match)[word_index]


def time(match, player_num, word_index):
    """A utility function for the time it took player_num to type the word at word_index"""
    assert word_index < len(get_all_words(match)), "word_index out of range of words"
    assert player_num < len(get_all_times(match)), "player_num out of range of players"
    return get_all_times(match)[player_num][word_index]

def get_all_words(match):
    """A selector function for all the words in the match"""
    return match["words"]

def get_all_times(match):
    """A selector function for all typing times for all players"""
    return match["times"]


def match_string(match):
    """A helper function that takes in a match data abstraction and returns a string representation of it"""
    return f"match({get_all_words(match)}, {get_all_times(match)})"

enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        source = pick(paragraphs, select, i)
        if not source:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(source)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, source))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)