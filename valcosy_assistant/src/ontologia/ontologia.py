from datetime import date

# Clases
hoteles = []
habitaciones = []
clientes = []
reservas = []
formularios = []
metodos_pago = []

# Propiedades
precios_habitaciones = {}
tipos_habitaciones = {}
disponibilidad_habitaciones = {}
fechas_entrada_reservas = {}
fechas_salida_reservas = {}
clientes_reservas = {}
habitaciones_reservas = {}
metodos_pago_reservas = {}

# Relaciones
selecciones_cliente = {}
formularios_cliente = {}
metodos_pago_cliente = {}
reservas_habitacion = {}
reservas_cliente = {}

# Instancias de clases y hechos
hoteles.append('hotel_abc')
habitaciones.append('Habitación suite 101')
habitaciones.append('Habitación estándar 205')
habitaciones.append('Habitación suite 403')
clientes.append('juan')
reservas.append('res_001')
formularios.append('form_001')
metodos_pago.append('visa')
precios_habitaciones['Habitación suite 101'] = 100
tipos_habitaciones['Habitación suite 101'] = 'individual'
disponibilidad_habitaciones['Habitación suite 101'] = [(date(2023, 5, 1), date(2023, 5, 3))]
disponibilidad_habitaciones['Habitación estándar 205'] = [(date(2023, 5, 1), date(2023, 5, 3))]
disponibilidad_habitaciones['Habitación suite 403'] = [(date(2023, 5, 1), date(2023, 5, 3))]
fechas_entrada_reservas['res_001'] = date(2023, 5, 1)
fechas_salida_reservas['res_001'] = date(2023, 5, 3)
clientes_reservas['res_001'] = 'juan'
habitaciones_reservas['res_001'] = 'Habitación suite 101'
metodos_pago_reservas['res_001'] = 'visa'
selecciones_cliente['juan'] = ['Habitación suite 101']
formularios_cliente['juan'] = ['form_001']
metodos_pago_cliente['juan'] = ['visa']
reservas_habitacion['Habitación suite 101'] = ['res_001']
reservas_cliente['juan'] = ['res_001']

# Reglas
def reserva_valida(reserva):
    if (
        reserva in fechas_entrada_reservas
        and reserva in fechas_salida_reservas
        and reserva in clientes_reservas
        and reserva in habitaciones_reservas
        and reserva in metodos_pago_reservas
        and clientes_reservas[reserva] in clientes
        and habitaciones_reservas[reserva] in habitaciones
        and metodos_pago_reservas[reserva] in metodos_pago
        and fechas_entrada_reservas[reserva] in [fecha[0] for fecha in disponibilidad_habitaciones[habitaciones_reservas[reserva]]]
        and fechas_salida_reservas[reserva] in [fecha[1] for fecha in disponibilidad_habitaciones[habitaciones_reservas[reserva]]]
    ):
        return True
    return False

def habitacion_disponible(habitacion, fecha_entrada, fecha_salida):
    disponibilidad = disponibilidad_habitaciones.get(habitacion, [])
    for fecha_range in disponibilidad:
        if (fecha_salida < fecha_range[0] or fecha_entrada > fecha_range[1]):
            return True
    return False

def precio_total(reserva):
    habitacion = habitaciones_reservas[reserva]
    precio_noche = precios_habitaciones[habitacion]
    fecha_entrada = fechas_entrada_reservas[reserva]
    fecha_salida = fechas_salida_reservas[reserva]
    dias_reserva = (fecha_salida - fecha_entrada).days
    return precio_noche * dias_reserva

def reservas_cliente_func(cliente):
    return reservas_cliente.get(cliente, [])

def habitaciones_disponibles(fecha_entrada, fecha_salida):
    habitaciones_disponibles = []
    for habitacion in habitaciones:
        if habitacion_disponible(habitacion, fecha_entrada, fecha_salida):
            habitaciones_disponibles.append(habitacion)
    return habitaciones_disponibles


print(reserva_valida('res_001'))  # Output: True
print(precio_total('res_001'))  # Output: 200
print(reservas_cliente_func('juan'))  # Output: ['res_001']
print(habitaciones_disponibles(date(2023, 5, 15), date(2023, 5, 18)))