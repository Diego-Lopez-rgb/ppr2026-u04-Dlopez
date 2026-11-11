import ipaddress
from pathlib import Path

dispositivos=[
    {
        "nombre": "Router01",
        "interfaz": "G0/0",
        "ip": "192.168.1.1",
        "mascara": "255.255.255.0"
    },
    {
        "nombre": "Router02",
        "interfaz": "G0/0",
        "ip": "192.168.2.1",
        "mascara": "255.255.255.0"
    },
    {
        "nombre": "SwitchCore",
        "interfaz": "VLAN10",
        "ip": "192.168.10.2",
        "mascara": "255.255.255.0"
    },
    {
        "nombre": "FirewallEdge",
        "interfaz": "G0/1",
        "ip": "10.0.0.256",
        "mascara": "255.0.0.0"
    },
    {
        "nombre": "ServidorDNS",
        "interfaz": "Eth0",
        "ip": "192.168.2.1",
        "mascara": "255.255.255.0"
    },
    {
        "nombre": "AccessPoint01",
        "interfaz": "BVI1",
        "ip": "172.16.5.10",
        "mascara": "255.255.0.0"
    },
    {
        "nombre": "RouterBranch",
        "interfaz": "S0/0/0",
        "ip": "192.168.100.999",
        "mascara": "255.255.255.0"
    },
    {
        "nombre": "ServidorSQL",
        "interfaz": "Eth1",
        "ip": "192.168.20.15",
        "mascara": "255.255.255.0"
    },
    {
        "nombre": "SwitchAccess",
        "interfaz": "VLAN1",
        "ip": "192.168.1.254",
        "mascara": "255.255.255.0"
    },
    {
        "nombre": "GatewayVoz",
        "interfaz": "G0/2",
        "ip": "172.16.1.1",
        "mascara": "255.255.255.128"
    }
]

ips_registradas = []
ips_validas = 0
ips_invalidas = 0
ips_duplicadas = 0

for dispositivo in dispositivos:
    ip = dispositivo["ip"]
    nombre = dispositivo["nombre"]

    try:
        ipaddress.ip_address(ip)

        if ip in ips_registradas:
            print(nombre, "-", ip, "DIRECCIÓN IP DUPLICADA")
            ips_duplicadas+=1
        else:
            ips_registradas.append(ip)
            print(nombre, "-", ip, "DIRECCIÓN IP VÁLIDA")
            ips_validas+=1

    except ValueError:
        print(nombre, "-", ip, "DIRECCIÓN IP INVÁLIDA")
        ips_invalidas+=1

print("válidas:", ips_validas)
print("inválidas:", ips_invalidas)
print("duplicadas:", ips_duplicadas)

#crear carpeta con los de configuracion

carpeta = Path("configuracion")
carpeta.mkdir(exist_ok=True)

#Generar la config solo para las IP válidas
if ips_validas > 0:
    for ip_valida in ips_registradas:
        for dispositivo in dispositivos:
            if dispositivo["ip"] == ip_valida:
                configuracion = f'''
hostname {dispositivo["nombre"]}
interface {dispositivo["interfaz"]}
ip address {dispositivo["ip"]} {dispositivo["mascara"]}
no shutdown
end
'''
                archivo = carpeta / f'{dispositivo["nombre"]}.txt'
                archivo.write_text(configuracion, encoding="utf-8")
                break

            