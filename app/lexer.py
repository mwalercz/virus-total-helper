import ply.lex as lex


class Lexer:
    states = (
        ('insidequotes', 'exclusive'),
        ('insidetag', 'exclusive'),
        ('script', 'exclusive')
    )
    tokens = (
        'OPEN_DASH',
        'OPEN',
        'CLOSE',
        'ASSIGN',
        'QUOTE',
        'WORD'
    )

    # wewnatrz script
    def t_script_WORD(self, t):
        r'[^< ]+'

    def t_script_OPEN_DASH(self, t):
        r'</'

    # wewnatrz ""
    def t_insidequotes_WORD(self, t):
        r'[^" ]+'

    def t_insidequotes_QUOTE(self, t):
        r'"'
        t.lexer.begin("insidetag")

    # wewnatrz <>
    def t_insidetag_CLOSE(self, t):
        r'>'
        t.lexer.begin('INITIAL')

    def t_insidetag_ASSIGN(self, t):
        r'='

    def t_insidetag_QUOTE(self, t):
        r'"'
        t.lexer.begin('insidequotes')

    def t_insidetag_WORD(self, t):
        r'[^>"= ]+'

    # na zewnatrz <>
    def t_INITIAL_OPEN(self, t):
        r'<'
        t.lexer.begin("insidetag")

    def t_INITIAL_WORD(self, t):
        r'[^< ]+'

    # zawsze
    def t_ANY_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ANY_ignore = ' \t'

    def t_ANY_error(self, t):
        print("Illegal character '%s'" % t[0])
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self,  **kwargs)

    def input(self, data):
        self.lexer.input(data)

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


if "__main__" == "__name":
    m = Lexer()
    m.build()  # Build the lexer

    m.test('''
    <body>
      <div class="wrapper">
        <div id="cookies-disabled-alert" class="alert center hide"
             style="margin: 55px auto 0; width: 600px;">
          <a class="close" data-dismiss="alert">×</a>
          <strong>Obsługa plików cookie w przeglądarce jest wyłączona!</strong>
          Ta strona wymaga włączonej obsługi plików cookie, aby działać poprawnie
        </div>

        <div class="navbar navbar-fixed-top">
          <div class="navbar-inner">
            <div class="container">



    <ul class="nav">
      <li id="mnu-home">
            <a href="/pl/" alt="home" title="Home"><i class="icon-home icon-white" alt="home" title="Home"></i></a>
        </li>
      <li id="mnu-community">
        <a href="/pl/community/">Społeczność</a>
      </li>
      <li id="mnu-statistics">
        <a href="/pl/statistics/">Statystyki</a>
      </li>
      <li id="mnu-documentation" class="dropdown">
        <a href="/pl/documentation/">Dokumentacja</a>
      </li>
      <li id="mnu-faq">
        <a href="/pl/faq/">FAQ</a>
      </li>
      <li id="mnu-about">
        <a href="/pl/about/">O VirusTotal</a>
      </li>
    </ul>


      <ul class="nav pull-right">


        <li>
          <a id="mnu-join" data-toggle="modal" data-backdrop="static"
             data-keyboard="true" href="#dlg-join">
            Dołącz do społeczności
          </a>
        </li>
        <li id="mnu-signin" class="">
          <a data-toggle="modal" data-backdrop="static"
             data-keyboard="true" href="#dlg-signin">
            Zaloguj się
          </a>
        </li>

      </ul>

    ''')
