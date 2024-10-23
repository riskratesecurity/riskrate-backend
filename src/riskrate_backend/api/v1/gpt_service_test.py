from io import BytesIO
from fastapi import APIRouter,  Response, BackgroundTasks
from riskrate_backend.services.gpt_model_service import GptModelService
from riskrate_backend.services.pdf_service import PDF

router = APIRouter()

@router.get("/pdf")
def get_pdf(background_tasks: BackgroundTasks):
    model = GptModelService()
    perguntas = [
        "Como o Google Cloud garante a disponibilidade e confiabilidade de seus serviços para manter a qualidade do software que roda na nuvem?",
        "Quais medidas de segurança são implementadas para proteger o software na Google Cloud contra vulnerabilidades de rede e ataques cibernéticos, como DDoS e injeção de código malicioso?",
        "Como o Google Cloud facilita a conformidade com padrões de segurança e auditorias para garantir que o software atende aos requisitos regulatórios (como GDPR, HIPAA)?"
    ]
    text = model.generate_text(perguntas)
    # text = [{'question_number': 1, 'question': 'Como o Google Cloud garante a disponibilidade e confiabilidade de seus serviços para manter a qualidade do software que roda na nuvem?', 'response': 'O Google Cloud garante a disponibilidade e confiabilidade dos serviços através de uma estrutura robusta de data centers, redundância, monitoramento proativo e suporte ao cliente 24/7.', 'explanation': 'Essas características são fundamentais para evitar tempo de inatividade e garantir que a empresa possa contar com a infraestrutura em nuvem sempre que necessário.', 'suggestions': [{'suggestion': 'Implemente um plano de continuidade de negócios (BCP) abrangente que inclua redundância de sistemas e recuperação de desastres.'}, {'suggestion': 'Utilize serviços de multi-zona para distribuir a carga e minimizar a dependência de um único ponto de falha.'}, {'suggestion': 'Adote práticas de monitoramento em tempo real para detectar e responder rapidamente a quaisquer interrupções.'}, {'suggestion': 'Regularmente teste seus processos de recuperação de desastres para assegurar que estão prontos para serem acionados quando necessário.'}, {'suggestion': 'Considere a implementação de um serviço de CDN (Content Delivery Network) para melhorar a entrega de conteúdo e a confiabilidade.'}]}, {'question_number': 2, 'question': 'Quais medidas de segurança são implementadas para proteger o software na Google Cloud contra vulnerabilidades de rede e ataques cibernéticos, como DDoS e injeção de código malicioso?', 'response': 'Medidas como firewalls, sistemas de prevenção de intrusões (IPS), autenticação multifator (MFA) e atualizações regulares de segurança são implementadas no Google Cloud.', 'explanation': 'Essas medidas são essenciais para proteger o ambiente em nuvem contra diversos tipos de ataques cibernéticos.', 'suggestions': [{'suggestion': 'Implemente firewalls de nova geração e sistemas de DPI (Deep Packet Inspection) para monitorar e filtrar o tráfego de rede.'}, {'suggestion': 'Adote autenticação multifator (MFA) para todas as contas de acesso ao sistema na nuvem.'}, {'suggestion': 'Realize testes de penetração regulares para identificar e corrigir vulnerabilidades em seu software.'}, {'suggestion': 'Eduque sua equipe sobre as melhores práticas de segurança e como evitar phishing e engenharia social.'}, {'suggestion': 'Utilize ferramentas de monitoramento de segurança para detectar padrões de tráfego incomuns que poderiam indicar um ataque DDoS.'}]}, {'question_number': 3, 'question': 'Como o Google Cloud facilita a conformidade com padrões de segurança e auditorias para garantir que o software atende aos requisitos regulatórios (como GDPR, HIPAA)?', 'response': 'O Google Cloud oferece certificações de conformidade, ferramentas de auditoria e suporte para atender a requisitos regulatórios como GDPR e HIPAA, ajudando os clientes a manter a conformidade.', 'explanation': 'A conformidade é crítica para garantir a proteção de dados e a continuidade do negócio em setores regulados, e o Google Cloud oferece suporte abrangente para isso.', 'suggestions': [{'suggestion': 'Realize uma análise regular de conformidade para assegurar que os sistemas estão alinhados com os requisitos regulatórios.'}, {'suggestion': 'Utilize serviços de criptografia para proteger dados em trânsito e em repouso.'}, {'suggestion': 'Implementar um plano de gestão da privacidade para assegurar que todas as práticas estão em conformidade com regulamentos como GDPR.'}, {'suggestion': 'Organizar auditorias internas trimestrais para revisar e verificar os processos de conformidade.'}, {'suggestion': 'Eduque a equipe sobre as leis de proteção de dados e como essas podem impactar os processos internos da empresa.'}]}]
    headers = {'Content-Disposition': 'inline; filename="out.pdf"'}
    print(text)
    pdf_output = generate_pdf(text)
    return Response(pdf_output.read(), headers=headers, media_type='application/pdf')

def generate_pdf(text: dict):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for txt in text:
        pdf.multi_cell(190, 10, txt=f"{txt['question_number']} - {txt['question']}", border=1)
        pdf.multi_cell(190, 10, txt=f"Resposta: {txt['response']}\nExplicação: {txt['explanation']}", border=1)
        
    pdf_output = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)

    return pdf_output