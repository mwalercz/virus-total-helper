import ply.yacc as yacc

from app.lexer import Lexer


class Tag:
    def __init__(self, tagname, attributes={}):
        self.tagname = tagname
        self.attributes = attributes


    def __repr__(self):
        return "TAG: { " \
               "tagname: " + self.tagname + \
               ", attributes: " + str(self.attributes) + "}\n"

    # def __eq__(self, other):
    #     if self.tagname == other.tagname:
    #         for attribute in self.attributes:
    #             if other.attributes[attribute] != self.attributes[attribute]:
    #                 return False
    #         return True
    #     else:
    #         return False


class Content:
    def __init__(self, head, rest=None):
        if rest is None:
            self.content = head
        else:
            self.content = head + " " + str(rest)

    def __str__(self):
        return self.content

    def __repr__(self):
        return "CONTENT: {" + self.content + "}\n"


class Parser:
    def __init__(self):
        self.element_list = []
        self.tokens = Lexer.tokens
        self.parser = yacc.yacc(module=self)

    def parse(self, data):
        lexer = Lexer()
        lexer.build()
        lexer.input(data)
        self.parser.parse(lexer=lexer.lexer, debug=True)
        self.element_list.reverse()
        return self.element_list

    def p_element(self, p):
        '''element : tag
                   | content
                   | close_tag
                   | close_tag element
                   | tag element
                   | content element '''
        p[0] = p[1]
        self.element_list.append(p[1])

    def p_tag(self, p):
        '''tag : OPEN tagname attributes CLOSE
               | OPEN tagname CLOSE'''
        if len(p) == 5:
            p[0] = Tag(p[2], p[3])
        else:
            p[0] = Tag(p[2])

        if p[0].tagname == "script":
            p.lexer.begin("script")

    def p_close_tag(self, p):
        '''close_tag : OPEN_DASH tagname CLOSE'''

        p[0] = Tag(p[2])
        if p[0].tagname == 'script':
            p.lexer.begin("INITIAL")

    def p_tagname(self, p):
        '''tagname : WORD'''
        p[0] = p[1]

    def p_attributes(self, p):
        '''attributes : attribute
                      | attribute attributes'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[2]
            p[2].update(p[1])

    def p_attribute(self, p):
        '''attribute : WORD ASSIGN QUOTE content QUOTE
                | WORD '''
        if len(p) == 6:
            p[0] = {p[1]: str(p[4])}
        else:
            p[0] = {p[1]: p[1]}

    def p_content(self, p):
        '''content : WORD
                   | WORD content'''
        if len(p) == 2:
            p[0] = Content(p[1])
        else:
            p[0] = Content(p[1], p[2])

    def p_error(self, p):
        print("Syntax error in input! " + str(p))


