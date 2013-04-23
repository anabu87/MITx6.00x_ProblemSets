# 6.00x Problem Set 5
#
# Part 2 - RECURSION

#
# Problem 3: Recursive String Reversal
#
def reverseString(aStr):
    """
    Given a string, recursively returns a reversed copy of the string.
    For example, if the string is 'abc', the function returns 'cba'.
    The only string operations you are allowed to use are indexing,
    slicing, and concatenation.
    
    aStr: a string
    returns: a reversed string
    """
    ### TODO.
    if not aStr:
        return ''
    if len(aStr) == 1:
        return aStr
    return aStr[-1] + reverseString(aStr[:-1])
#
# Problem 4: X-ian
#
def x_ian(x, word):
    """
    Given a string x, returns True if all the letters in x are
    contained in word in the same order as they appear in x.

    >>> x_ian('eric', 'meritocracy')
    True
    >>> x_ian('eric', 'cerium')
    False
    >>> x_ian('john', 'mahjong')
    False
    
    x: a string
    word: a string
    returns: True if word is x_ian, False otherwise
    """
    ###TODO.
    if not x:
        return True
    if len(x) == 1:
        return (x in word)
    return (x[0] in word) and x_ian(x[1:], word[word.find(x[0]) + 1:])    

#
# Problem 5: Typewriter
#
def insertNewlines(text, lineLength):
    """
    Given text and a desired line length, wrap the text as a typewriter would.
    Insert a newline character ("\n") after each word that reaches or exceeds
    the desired line length.

    text: a string containing the text to wrap.
    line_length: the number of characters to include on a line before wrapping
        the next word.
    returns: a string, with newline characters inserted appropriately. 
    """
    ### TODO.
    if len(text) < lineLength:
        return text
    if not text[lineLength - 1].isspace():
        index = text[lineLength:].find(' ')
        if index == -1:
            return text
        return text[:lineLength+index+1] + '\n' + insertNewlines(text[lineLength+index+1:], lineLength)
    return text[:lineLength] + '\n' + insertNewlines(text[lineLength:], lineLength)

if __name__ == '__main__':
    print insertNewlines('While I expect new intellectual adventures ahead, nothing will compare to the exhilaration of the world-changing accomplishments that we produced together.', 15)
    print 
    print insertNewlines('Nuh-uh! We let users vote on comments and display them by number of votes. Everyone knows that makes it impossible for a few persistent voices to dominate the discussion.', 20)
    print
    print insertNewlines('Random text to wrap again.', 5)
    print
    print insertNewlines('usrdzv alqf xhq nkt netuq jcpn der ejnd aurqjs iajunrwk qihz sikudf zilkbsj', 43)
    print
    print insertNewlines('epruf jfw dko sgciofr asu spivqh chzp fszecrw oidy uxoy qgy uzd ulyr qhyie ghljr gkjblnt', 29)
    print
    print insertNewlines('gspx sfkdcgv byzlwv fzt eriknyxh ftioqxl azimfyl xukl lex kpvdbzg tfvjn ulwdty tksmgc qxeintfr vdqf nrdgil ahjrlvp bromipc xnhaeq rtzfoq aycozdw jnm smbxyl foq', 43)
    print
    print insertNewlines('flgobs oeduf vnwba vlap wnohbaqs gxvwl edo rpu wokfa rsieo qcu vuhxr cvzpsgo cthko upravjfe cuefrzg faydg jquizvp ugomrek bzaypc jyhonaqu ubf sqx cwqidztu ned leiwbto', 23)
    print
    print insertNewlines('nbcphfls vszr bwuypq rls qsikrm xzlebk ztkmbfl ksm liv jrqfhia ifa', 50)
    