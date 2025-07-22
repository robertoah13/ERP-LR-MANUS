import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Settings } from 'lucide-react'

export default function Producao() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Produção</h1>
        <p className="text-muted-foreground">
          Controle o fluxo de produção das próteses
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Settings className="mr-2 h-5 w-5" />
            Módulo de Produção
          </CardTitle>
          <CardDescription>
            Esta funcionalidade está em desenvolvimento
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <Settings className="mx-auto h-12 w-12 text-muted-foreground" />
            <h3 className="mt-2 text-sm font-semibold text-gray-900">Módulo em Desenvolvimento</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              O módulo de produção será implementado em breve com controle de etapas, Kanban e estatísticas de produtividade.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

