# Assinatura-gen
Esse repositório hospeda o código do Gerador de assinaturas de e-mail dos colaboradores da QUICK FIBRA. A manutenção da criação de assinaturas de e-mails é desgastante, pois com mudanças no quadro de colaboradores e na mudança de cargos, é necessário criar / excluir / alterar as assinaturas, que são editadas por uma agência de marketing. Eu criei esse APP para que o gestor de cada colaborador seja capaz de editar a própria assinatura, sob supervisão de seu gestor. Dessa forma, fica muito mais fácil manter tudo atualizado, principalmente com o crescimento do quadro de colaboradores.

![Minha assinatura como exemplo](assinaturas_ex/lucasrochaabraao.png)

Status atual (em desenvolvimento):
Já existe uma página web através do django que permite criar itens (assinaturas). Porém ainda não implementei os scripts que geram as assinaturas nos views do django. Se rodar o script encontrado em `Assinaturas_scripts` é possível gerar as assinaturas automaticamente através do terminal mesmo. Ou seja, já consigo automatizar a geração de criação/modificação de assinaturas, porém a parte web onde o próprio colaborador vai interagir não está pronto.
