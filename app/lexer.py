import ply.lex as lex



class Lexer:


    tokens = (
        'OPEN',
        'CLOSE',
        'ASSIGN',
        'QUOTE',
        'WORD'
    )

    t_OPEN = r'<'
    t_CLOSE = r'>'
    t_ASSIGN = r'='
    t_QUOTE = r'"'
    t_WORD = r'[^><"= ]+'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t'

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

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
