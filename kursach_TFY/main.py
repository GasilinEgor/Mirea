import LexicalAnalyzer
import Parser


def main():
    program = input("Введите название файла: ")
    lexer = LexicalAnalyzer.Lexer(program)
    lexer.lexer()
    file_name = lexer.print_tokens_in_text()
    parser = Parser.Parse(file_name)
    parser.program()


if __name__ == '__main__':
    main()
