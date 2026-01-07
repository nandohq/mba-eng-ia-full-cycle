import sys
from .search import search_prompt, search_results

def main():
    chain = search_prompt()
    header_text = "🤖 Chatnator"
    header_length = 60
    header_space = (header_length - len(header_text)) // 2
    
    print("\n" + "="*header_length, file=sys.stdout)
    print(" "*header_space + "🤖 Chatnator" + " "*header_space, file=sys.stdout)
    print("="*header_length, file=sys.stdout)
    print("Pergunte algo ou digite 'exit'|'quit'|'sair'", file=sys.stdout)
    print("="*header_length, file=sys.stdout)
   
    while True:
        question = input("\nPERGUNTA: ")
        
        if question.lower() in ["exit", "quit", "sair"]:
            print("\n Até logo!")
            print("="*header_length, file=sys.stdout)
            sys.exit(0)

        if not question.strip():
            print("\nPor favor, digite uma pergunta válida!")
            continue

        try:
            results = search_results(question=question)

            if not results:
                print("\nNão foi possível encontrar informações relevantes para a pergunta.")
                continue
            
            context = "\n\n".join([
                doc.page_content 
                for doc, _ in results
            ])
            
            response = chain.invoke({"contexto": context, "pergunta": question})
            
            print(f"\nRESPOSTA: {response.content}")
        
        except (KeyboardInterrupt, EOFError):
            print("\n Até logo!")
            print("="*header_length, file=sys.stdout)
            sys.exit(0)
        except Exception as ex:
            print("\n" + "="*header_length, file=sys.stderr)
            print("Erro: não pude processar a pergunta!", file=sys.stderr)
            print("="*header_length, file=sys.stderr)
            print(f"\n{str(ex)}", file=sys.stderr)
            print("\n" + "-"*header_length, file=sys.stderr)

            sys.exit(1)

if __name__ == "__main__":
    main()