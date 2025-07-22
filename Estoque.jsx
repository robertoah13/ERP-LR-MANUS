import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Package } from 'lucide-react'

export default function Estoque() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Estoque</h1>
        <p className="text-muted-foreground">
          Gerencie materiais e insumos do laboratório
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Package className="mr-2 h-5 w-5" />
            Módulo de Estoque
          </CardTitle>
          <CardDescription>
            Esta funcionalidade está em desenvolvimento
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <Package className="mx-auto h-12 w-12 text-muted-foreground" />
            <h3 className="mt-2 text-sm font-semibold text-gray-900">Módulo em Desenvolvimento</h3>
            <p className="mt-1 text-sm text-muted-foreground">
              O módulo de estoque será implementado em breve com controle de materiais, movimentações e alertas de estoque mínimo.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

