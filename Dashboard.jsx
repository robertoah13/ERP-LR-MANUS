import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  Users, 
  UserCheck, 
  FileText, 
  AlertTriangle, 
  DollarSign, 
  Package,
  Calendar,
  TrendingUp
} from 'lucide-react'

export default function Dashboard() {
  const [resumo, setResumo] = useState(null)
  const [alertas, setAlertas] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulação de dados - em produção, fazer chamadas para API
    setTimeout(() => {
      setResumo({
        clientes: { total: 45 },
        pacientes: { total: 128 },
        ordens_servico: {
          total: 89,
          recebidas: 12,
          em_producao: 23,
          finalizadas: 8,
          entregues: 46,
          atrasadas: 3
        },
        financeiro: {
          total_a_receber: 15750.00,
          total_a_pagar: 8200.00,
          faturamento_mes: 32500.00
        },
        estoque: {
          materiais_criticos: 5
        },
        agenda: {
          eventos_hoje: 4
        }
      })

      setAlertas([
        {
          tipo: 'warning',
          titulo: 'Ordens Atrasadas',
          mensagem: '3 ordem(ns) de serviço em atraso',
          link: '/ordens-servico?status=atrasadas'
        },
        {
          tipo: 'danger',
          titulo: 'Estoque Crítico',
          mensagem: '5 material(is) com estoque baixo',
          link: '/estoque/materiais?critico=true'
        },
        {
          tipo: 'info',
          titulo: 'Eventos Hoje',
          mensagem: '4 evento(s) agendado(s) para hoje',
          link: '/agenda/hoje'
        }
      ])

      setLoading(false)
    }, 1000)
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Carregando dashboard...</div>
      </div>
    )
  }

  const getAlertVariant = (tipo) => {
    switch (tipo) {
      case 'danger': return 'destructive'
      case 'warning': return 'secondary'
      case 'info': return 'default'
      default: return 'default'
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Visão geral do laboratório LR Prótese Dental
        </p>
      </div>

      {/* Cards de Resumo */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Clientes</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{resumo.clientes.total}</div>
            <p className="text-xs text-muted-foreground">
              Dentistas e clínicas cadastradas
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Pacientes</CardTitle>
            <UserCheck className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{resumo.pacientes.total}</div>
            <p className="text-xs text-muted-foreground">
              Pacientes cadastrados
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Ordens em Produção</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{resumo.ordens_servico.em_producao}</div>
            <p className="text-xs text-muted-foreground">
              {resumo.ordens_servico.atrasadas} em atraso
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Faturamento do Mês</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              R$ {resumo.financeiro.faturamento_mes.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
            </div>
            <p className="text-xs text-muted-foreground">
              <TrendingUp className="inline h-3 w-3 mr-1" />
              +12% em relação ao mês anterior
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Alertas */}
      {alertas.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <AlertTriangle className="mr-2 h-5 w-5" />
              Alertas e Notificações
            </CardTitle>
            <CardDescription>
              Itens que requerem sua atenção
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {alertas.map((alerta, index) => (
                <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                  <div>
                    <div className="font-medium">{alerta.titulo}</div>
                    <div className="text-sm text-muted-foreground">{alerta.mensagem}</div>
                  </div>
                  <Badge variant={getAlertVariant(alerta.tipo)}>
                    {alerta.tipo === 'danger' ? 'Crítico' : 
                     alerta.tipo === 'warning' ? 'Atenção' : 'Info'}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Resumo Detalhado */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <FileText className="mr-2 h-5 w-5" />
              Ordens de Serviço
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm">Recebidas</span>
                <Badge variant="secondary">{resumo.ordens_servico.recebidas}</Badge>
              </div>
              <div className="flex justify-between">
                <span className="text-sm">Em Produção</span>
                <Badge variant="default">{resumo.ordens_servico.em_producao}</Badge>
              </div>
              <div className="flex justify-between">
                <span className="text-sm">Finalizadas</span>
                <Badge variant="outline">{resumo.ordens_servico.finalizadas}</Badge>
              </div>
              <div className="flex justify-between">
                <span className="text-sm">Entregues</span>
                <Badge variant="outline">{resumo.ordens_servico.entregues}</Badge>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <DollarSign className="mr-2 h-5 w-5" />
              Financeiro
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm">A Receber</span>
                <span className="font-medium text-green-600">
                  R$ {resumo.financeiro.total_a_receber.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm">A Pagar</span>
                <span className="font-medium text-red-600">
                  R$ {resumo.financeiro.total_a_pagar.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                </span>
              </div>
              <div className="flex justify-between pt-2 border-t">
                <span className="text-sm font-medium">Saldo</span>
                <span className="font-bold text-blue-600">
                  R$ {(resumo.financeiro.total_a_receber - resumo.financeiro.total_a_pagar).toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Package className="mr-2 h-5 w-5" />
              Estoque & Agenda
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm">Materiais Críticos</span>
                <Badge variant="destructive">{resumo.estoque.materiais_criticos}</Badge>
              </div>
              <div className="flex justify-between">
                <span className="text-sm">Eventos Hoje</span>
                <Badge variant="default">{resumo.agenda.eventos_hoje}</Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

