from pydantic import BaseModel

from .dados_basicos_fatura import DadosBasicosFatura
from .pagamento import Pagamento
from .jira_info import JiraInfo

class Fatura(BaseModel):
    dados_basicos: DadosBasicosFatura
    pagamento: Pagamento

    def __init__(self, **data):
        super().__init__(**data)
        self.handleAllocationValue()

    def handleAllocationValue(self):
        if self.dados_basicos.valor_liquido:
            self.dados_basicos.handle_montante()
            for item in self.dados_basicos.itens:
                percentage = item.percentage
                valor_liquido_total = self.dados_basicos.valor_liquido
                item.valor_liquido = valor_liquido_total * (percentage / 100)
                item.handle_montante()
        pass
