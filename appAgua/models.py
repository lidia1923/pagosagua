from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class Persona(models.Model):
    nombres = models.CharField(max_length=250)
    apellidos = models.CharField(max_length=250)
    cedula = models.CharField(max_length=10)
    celular = models.CharField(max_length=10)
    correo = models.EmailField()

class Tesorero(Persona):
    idTesorero = models.AutoField(primary_key=True)
    estado = models.BooleanField('Estado', default=True)

    def __str__(self):
        return (self.nombres+' '+self.apellidos)

    class Meta:
        verbose_name = 'Tesorero'
        verbose_name_plural = 'Tesoreros'

class Usuario(Persona):
    idUsuario = models.AutoField(primary_key=True)
    usuarioAgua = models.OneToOneField(User, on_delete=models.CASCADE, default="")

    def __str__(self):
        return (self.nombres+' '+self.apellidos)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Pago(models.Model):
    idPago = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tesorero = models.ForeignKey(Tesorero, on_delete=models.CASCADE)
    mesDesde = models.DateField()
    mesHasta = models.DateField()
    costoServicio = models.DecimalField(decimal_places=2, max_digits=4)

    def __str__(self):
        return self.usuario.nombres

    class Meta:
        verbose_name = 'Pago de Agua'
        verbose_name_plural = 'Pagos de Agua'

class ServicioAgua(models.Model):
    idServicioAgua = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    costoActivacion = models.DecimalField(decimal_places=2, max_digits=4)
    motivoSuspension = models.TextField()
    estado = models.BooleanField('Estado', default=True)

    def __str__(self):
        return self.usuario.nombres

    class Meta:
        verbose_name = 'Servicio de Agua'
        verbose_name_plural = 'Servicios de Agua'

class HistorialServicio(models.Model):
    idHistorial = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=250)
    costoActivacion = models.DecimalField(decimal_places=2, max_digits=4)
    motivoSuspension = models.TextField()
    fechaSuspension = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.usuario

    class Meta:
        verbose_name = 'Historial de Servicio'
        verbose_name_plural = 'Historial de Servicios'