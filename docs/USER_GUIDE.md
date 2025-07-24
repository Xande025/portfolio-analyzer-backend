# 📖 Guia do Usuário - Analisador de Portfólio

Este guia completo irá ajudá-lo a aproveitar ao máximo todas as funcionalidades do Analisador de Portfólio.

## 🏠 Dashboard Principal

O Dashboard é o centro de controle da sua análise de investimentos.

### Métricas Principais
- **Retorno Anual**: Retorno esperado do portfólio em base anual
- **Volatilidade**: Medida de risco (desvio padrão dos retornos)
- **Índice Sharpe**: Retorno ajustado ao risco (quanto maior, melhor)
- **Máximo Drawdown**: Maior perda consecutiva do portfólio

### Gráficos Disponíveis
1. **Alocação do Portfólio**: Gráfico de pizza mostrando distribuição dos ativos
2. **Retornos dos Ativos**: Barras comparando retornos anualizados
3. **Volatilidade dos Ativos**: Barras mostrando risco de cada ativo
4. **Matriz de Correlação**: Heatmap das correlações entre ativos

## 🔍 Buscar Ativos

### Como Buscar
1. Acesse a página "Buscar Ativos"
2. Digite o símbolo (ex: AAPL) ou nome da empresa
3. Selecione o tipo de ativo (opcional)
4. Clique em "Buscar"

### Tipos de Ativos Suportados
- **Ações**: Empresas listadas em bolsas globais
- **Criptomoedas**: Bitcoin, Ethereum, e outras
- **Fundos**: ETFs e fundos de investimento

### Adicionando ao Portfólio
1. Encontre o ativo desejado nos resultados
2. Clique em "Adicionar"
3. O ativo aparecerá na seção "Ativos Selecionados"
4. Defina o peso (%) na página do Portfólio

## 💼 Construir Portfólio

### Definindo Pesos
1. Acesse a página "Portfólio"
2. Ajuste os pesos de cada ativo usando os sliders
3. Certifique-se que a soma seja 100%
4. As métricas são atualizadas automaticamente

### Removendo Ativos
- Clique no ícone de lixeira ao lado do ativo
- Confirme a remoção
- Os pesos são redistribuídos automaticamente

### Visualizando Detalhes
1. Clique em "Detalhes" em qualquer ativo
2. Visualize histórico de preços
3. Analise retornos diários
4. Veja estatísticas detalhadas

## 🎯 Otimização de Portfólio

### Fronteira Eficiente
A fronteira eficiente mostra todas as combinações ótimas de risco e retorno.

#### Como Usar:
1. Acesse "Otimização"
2. Certifique-se de ter pelo menos 2 ativos
3. Clique em "Otimizar"
4. Analise os resultados

### Portfólio de Máximo Sharpe
Este é o portfólio que oferece o melhor retorno ajustado ao risco.

#### Interpretando Resultados:
- **Alocação Recomendada**: Pesos ótimos para cada ativo
- **Métricas Esperadas**: Retorno, risco e Sharpe do portfólio ótimo
- **Comparação**: Como seu portfólio atual se compara ao ótimo

### Análise de Eficiência
- **Score de Eficiência**: 0-100% (quanto maior, melhor)
- **Rating**: Excelente (90%+), Boa (70-90%), Regular (50-70%), Precisa melhorar (<50%)
- **Recomendações**: Sugestões automáticas de melhoria

## 🔔 Alertas e Monitoramento

### Alertas de Preço
Configure notificações quando ativos atingirem preços específicos.

#### Criando Alertas:
1. Acesse "Alertas"
2. Selecione "Alerta de Preço"
3. Digite o símbolo do ativo
4. Defina o preço alvo
5. Escolha a condição (acima/abaixo)
6. Clique em "Criar Alerta"

### Alertas de Performance
Monitore métricas do seu portfólio automaticamente.

#### Métricas Disponíveis:
- **Retorno**: Quando retorno ultrapassar limite
- **Índice Sharpe**: Monitoramento de eficiência
- **Volatilidade**: Alertas de risco
- **Drawdown**: Notificações de perdas

### Monitoramento em Tempo Real
- Visualize preços atuais de todos os ativos
- Veja variações percentuais do dia
- Acompanhe volume de negociação
- Receba notificações de alertas acionados

### Gerenciando Alertas
- **Alertas Ativos**: Lista de alertas aguardando acionamento
- **Alertas Acionados**: Histórico dos últimos 7 dias
- **Remover Alertas**: Clique no ícone de lixeira

## 🎨 Personalização da Interface

### Tema Escuro/Claro
1. Clique no ícone de sol/lua no cabeçalho
2. A mudança é instantânea
3. Sua preferência é salva automaticamente

### Navegação
- Use o menu superior para alternar entre páginas
- Todas as páginas são responsivas
- Funciona perfeitamente em mobile e desktop

## 💡 Dicas e Melhores Práticas

### Construindo um Bom Portfólio
1. **Diversifique**: Use diferentes classes de ativos
2. **Correlação**: Evite ativos muito correlacionados
3. **Rebalanceamento**: Revise periodicamente os pesos
4. **Risco**: Considere sua tolerância ao risco

### Interpretando Métricas
- **Sharpe > 1.0**: Excelente retorno ajustado ao risco
- **Sharpe 0.5-1.0**: Bom desempenho
- **Sharpe < 0.5**: Considere otimização
- **Correlação > 0.7**: Ativos muito similares

### Usando Alertas Efetivamente
1. **Preços Realistas**: Defina alvos baseados em análise
2. **Múltiplos Alertas**: Configure para diferentes cenários
3. **Revisão Regular**: Atualize alertas conforme mercado
4. **Performance**: Monitore métricas-chave do portfólio

## ❓ Perguntas Frequentes

### Como adicionar ações brasileiras?
Digite o símbolo com ".SA" (ex: PETR4.SA, VALE3.SA)

### Por que alguns ativos não aparecem?
Verifique se o símbolo está correto e se o ativo é negociado publicamente.

### Como interpretar a matriz de correlação?
- Verde: Correlação positiva (ativos se movem juntos)
- Vermelho: Correlação negativa (ativos se movem opostamente)
- Intensidade da cor: Força da correlação

### Posso salvar múltiplos portfólios?
Atualmente, o sistema mantém um portfólio por sessão. Use exportação para salvar configurações.

### Os dados são em tempo real?
Sim, os preços são atualizados em tempo real via APIs financeiras.

## 🆘 Solução de Problemas

### Erro ao carregar dados
1. Verifique sua conexão com internet
2. Confirme se o símbolo do ativo está correto
3. Tente novamente após alguns segundos

### Gráficos não aparecem
1. Certifique-se de ter ativos no portfólio
2. Verifique se os pesos somam 100%
3. Recarregue a página se necessário

### Alertas não funcionam
1. Verifique se o símbolo está correto
2. Confirme se o preço alvo é realista
3. Use "Verificar" para testar manualmente

## 📞 Suporte

Para mais ajuda:
- Consulte a [Documentação da API](API_DOCS.md)
- Abra uma issue no GitHub
- Entre em contato: suporte@analisador-portfolio.com

---

**Aproveite ao máximo suas análises de investimento! 📈**

