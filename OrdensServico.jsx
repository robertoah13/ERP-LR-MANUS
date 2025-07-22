import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { FileText } from 'lucide-react'

export default function OrdensServico() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Ordens de Serviço</h1>
        <p className="text-muted-foreground">
          Gerencie as ordens de serviço do laboratório
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <FileText className="mr-2 h-5 w-5" />
            Módulo de Ordens de Serviço
          </CardTitle>
          <CardDescription>
            Esta funcionalidade está em desenvolvimento
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <FileText className="mx-auto h-12 w-12 text-muted-foreground" />
            <h3 className="mt-2 text-sm font-semibold text-gray-900">Módulo em Desenvolvimento</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              O módulo de ordens de serviço será implementado em breve com funcionalidades completas de gestão de trabalhos protéticos.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

