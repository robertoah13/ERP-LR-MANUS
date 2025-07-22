import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'
import { Plus, Search, Edit, Trash2, Users, Building } from 'lucide-react'

export default function Clientes() {
  const [clientes, setClientes] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [tipoFiltro, setTipoFiltro] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)
  const [editingCliente, setEditingCliente] = useState(null)
  const [formData, setFormData] = useState({
    nome: '',
    tipo: '',
    email: '',
    telefone: '',
    endereco: '',
    observacoes: ''
  })

  useEffect(() => {
    carregarClientes()
  }, [])

  const carregarClientes = () => {
    // Simulação de dados - em produção, fazer chamada para API
    setTimeout(() => {
      setClientes([
        {
          id: 1,
          nome: 'Dr. João Silva',
          tipo: 'dentista',
          email: 'joao.silva@email.com',
          telefone: '(11) 99999-9999',
          endereco: 'Rua das Flores, 123 - São Paulo/SP',
          observacoes: 'Cliente preferencial',
          ativo: true,
          data_cadastro: '2024-01-15T10:30:00'
        },
        {
          id: 2,
          nome: 'Clínica Odonto Vida',
          tipo: 'clinica',
          email: 'contato@odontovida.com',
          telefone: '(11) 88888-8888',
          endereco: 'Av. Paulista, 1000 - São Paulo/SP',
          observacoes: 'Clínica com 5 dentistas',
          ativo: true,
          data_cadastro: '2024-01-20T14:15:00'
        },
        {
          id: 3,
          nome: 'Dra. Maria Santos',
          tipo: 'dentista',
          email: 'maria.santos@email.com',
          telefone: '(11) 77777-7777',
          endereco: 'Rua Augusta, 500 - São Paulo/SP',
          observacoes: '',
          ativo: true,
          data_cadastro: '2024-02-01T09:00:00'
        }
      ])
      setLoading(false)
    }, 1000)
  }

  const clientesFiltrados = clientes.filter(cliente => {
    const matchSearch = cliente.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
                       cliente.email.toLowerCase().includes(searchTerm.toLowerCase())
    const matchTipo = !tipoFiltro || cliente.tipo === tipoFiltro
    return matchSearch && matchTipo
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    
    if (editingCliente) {
      // Atualizar cliente existente
      setClientes(clientes.map(cliente => 
        cliente.id === editingCliente.id 
          ? { ...cliente, ...formData }
          : cliente
      ))
    } else {
      // Criar novo cliente
      const novoCliente = {
        id: Date.now(),
        ...formData,
        ativo: true,
        data_cadastro: new Date().toISOString()
      }
      setClientes([...clientes, novoCliente])
    }
    
    resetForm()
  }

  const resetForm = () => {
    setFormData({
      nome: '',
      tipo: '',
      email: '',
      telefone: '',
      endereco: '',
      observacoes: ''
    })
    setEditingCliente(null)
    setDialogOpen(false)
  }

  const handleEdit = (cliente) => {
    setFormData({
      nome: cliente.nome,
      tipo: cliente.tipo,
      email: cliente.email,
      telefone: cliente.telefone,
      endereco: cliente.endereco,
      observacoes: cliente.observacoes
    })
    setEditingCliente(cliente)
    setDialogOpen(true)
  }

  const handleDelete = (id) => {
    if (confirm('Tem certeza que deseja excluir este cliente?')) {
      setClientes(clientes.filter(cliente => cliente.id !== id))
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg">Carregando clientes...</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Clientes</h1>
          <p className="text-muted-foreground">
            Gerencie dentistas e clínicas cadastradas
          </p>
        </div>
        
        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={() => resetForm()}>
              <Plus className="mr-2 h-4 w-4" />
              Novo Cliente
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[600px]">
            <DialogHeader>
              <DialogTitle>
                {editingCliente ? 'Editar Cliente' : 'Novo Cliente'}
              </DialogTitle>
              <DialogDescription>
                {editingCliente ? 'Atualize as informações do cliente' : 'Cadastre um novo cliente no sistema'}
              </DialogDescription>
            </DialogHeader>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="nome">Nome *</Label>
                  <Input
                    id="nome"
                    value={formData.nome}
                    onChange={(e) => setFormData({...formData, nome: e.target.value})}
                    placeholder="Nome do cliente"
                    required
                  />
                </div>
                
                <div>
                  <Label htmlFor="tipo">Tipo *</Label>
                  <Select value={formData.tipo} onValueChange={(value) => setFormData({...formData, tipo: value})}>
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione o tipo" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="dentista">Dentista</SelectItem>
                      <SelectItem value="clinica">Clínica</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="email">Email *</Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    placeholder="email@exemplo.com"
                    required
                  />
                </div>
                
                <div>
                  <Label htmlFor="telefone">Telefone</Label>
                  <Input
                    id="telefone"
                    value={formData.telefone}
                    onChange={(e) => setFormData({...formData, telefone: e.target.value})}
                    placeholder="(11) 99999-9999"
                  />
                </div>
              </div>
              
              <div>
                <Label htmlFor="endereco">Endereço</Label>
                <Input
                  id="endereco"
                  value={formData.endereco}
                  onChange={(e) => setFormData({...formData, endereco: e.target.value})}
                  placeholder="Endereço completo"
                />
              </div>
              
              <div>
                <Label htmlFor="observacoes">Observações</Label>
                <Textarea
                  id="observacoes"
                  value={formData.observacoes}
                  onChange={(e) => setFormData({...formData, observacoes: e.target.value})}
                  placeholder="Observações sobre o cliente"
                  rows={3}
                />
              </div>
              
              <div className="flex justify-end space-x-2">
                <Button type="button" variant="outline" onClick={resetForm}>
                  Cancelar
                </Button>
                <Button type="submit">
                  {editingCliente ? 'Atualizar' : 'Cadastrar'}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Filtros */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Buscar por nome ou email..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            
            <Select value={tipoFiltro} onValueChange={setTipoFiltro}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Filtrar por tipo" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Todos os tipos</SelectItem>
                <SelectItem value="dentista">Dentista</SelectItem>
                <SelectItem value="clinica">Clínica</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Lista de Clientes */}
      <div className="grid gap-4">
        {clientesFiltrados.map((cliente) => (
          <Card key={cliente.id}>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    {cliente.tipo === 'dentista' ? (
                      <Users className="h-6 w-6 text-blue-600" />
                    ) : (
                      <Building className="h-6 w-6 text-blue-600" />
                    )}
                  </div>
                  
                  <div>
                    <div className="flex items-center space-x-2">
                      <h3 className="text-lg font-semibold">{cliente.nome}</h3>
                      <Badge variant={cliente.tipo === 'dentista' ? 'default' : 'secondary'}>
                        {cliente.tipo === 'dentista' ? 'Dentista' : 'Clínica'}
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground">{cliente.email}</p>
                    {cliente.telefone && (
                      <p className="text-sm text-muted-foreground">{cliente.telefone}</p>
                    )}
                    {cliente.endereco && (
                      <p className="text-sm text-muted-foreground">{cliente.endereco}</p>
                    )}
                  </div>
                </div>
                
                <div className="flex space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleEdit(cliente)}
                  >
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleDelete(cliente.id)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
              
              {cliente.observacoes && (
                <div className="mt-3 p-3 bg-gray-50 rounded-lg">
                  <p className="text-sm">{cliente.observacoes}</p>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {clientesFiltrados.length === 0 && (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-8">
              <Users className="mx-auto h-12 w-12 text-muted-foreground" />
              <h3 className="mt-2 text-sm font-semibold text-gray-900">Nenhum cliente encontrado</h3>
              <p className="mt-1 text-sm text-muted-foreground">
                {searchTerm || tipoFiltro ? 'Tente ajustar os filtros de busca.' : 'Comece cadastrando um novo cliente.'}
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

