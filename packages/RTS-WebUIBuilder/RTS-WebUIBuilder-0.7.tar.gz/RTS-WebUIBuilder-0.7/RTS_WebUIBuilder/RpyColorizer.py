from pygments.lexers import PythonLexer
from pygments.token import Token
from .RLabel import RLabel
from .RAdditions import rgb, rgba
def pylexerColorizer(code, filter: bool = False):
    
        def colorize(token: str, color: str):
            lable = RLabel("span")
            lable.displaytext = token
            lable.style.colorize(color=color)
            return lable._asm()

        # Verwende den PythonLexer von Pygments, um den Code zu analysieren und die Tokens zu extrahieren
        lexer = PythonLexer()
        tokens = lexer.get_tokens_unprocessed(code)
        previous_token_type = None
        previous_token_name = None

        

        # Durchlaufe die Tokens und färbe sie ein
        reformated_code = ""
        for i , token in enumerate(tokens):

            color = "white"
            skip = False
            _, ttype, token_value = token  

            if ttype in Token.Keyword or ttype in Token.Operator.Word or ttype in Token.Literal.String.Affix:
                color = rgb(255,45,46)
            if ttype in Token.Comment.Single:
                color = "gray"

            if ttype in Token.Name and not ttype in Token.Name.Function and not ttype in Token.Name.Class and not ttype in Token.Name.Builtin.Pseudo:
                skip = True
                
            
            if ttype in Token.Name.Function:
                color = rgb(210,168,242)

            if ttype in Token.Literal.String and not ttype in Token.Literal.String.Affix:
                color = rgb(112,198,240)
            
            
            if ttype in Token.Literal.Number.Integer:
                color = rgb(121,192,255)

            if ttype in Token.Text and not ttype in Token.Text.Whitespace:
                token_value = token_value.replace("  ", "&nbsp;&nbsp;&nbsp;")
                token_value = token_value.replace("\t", "&emsp;")
                color = rgba(0,0,0,0)

            if ttype in Token.Name.Class:
                color = rgb(255,123,84)
            
            if ttype in Token.Name.Builtin.Pseudo:
                color = "white"
            
            

            if previous_token_type in Token.Name and not ((ttype == Token.Punctuation and token_value == "(") or (ttype == Token.Operator and token_value == ".")):
                if not previous_token_type in Token.Name.Function and not previous_token_type in Token.Name.Class and not previous_token_type in Token.Name.Builtin.Pseudo:
                    reformated_code += colorize(previous_token_name, rgb(255,123,84))

            if previous_token_type is Token.Name and ttype == Token.Punctuation and token_value == "(":
                reformated_code += colorize(previous_token_name, rgb(210,168,242))

            if previous_token_type is Token.Name and (ttype == Token.Operator and token_value == "."):
                reformated_code += colorize(previous_token_name, "white")

            if ttype in Token.Text.Whitespace and token_value == "\n":
                token_value = "<br>"
                reformated_code += token_value
                skip = True

            if filter is True:
                with open("test.log","a") as f:
                    f.write(f"{ttype} -> '{token_value}'\n")

            previous_token_type = ttype
            previous_token_name = token_value

            if not skip:
                reformated_code += colorize(token_value, color)

        return reformated_code