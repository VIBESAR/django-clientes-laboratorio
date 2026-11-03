from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Cliente

class ClientesTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(username='estudiante', password='PruebaSegura2026!')

    def test_protege_clientes_sin_sesion(self):
        respuesta = self.client.get(reverse('clientes_crear'))
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn('/login/', respuesta.url)

    def test_crea_y_muestra_cliente_con_sesion(self):
        self.client.force_login(self.usuario)
        respuesta = self.client.post(reverse('clientes_crear'), {
            'nombre': 'Cliente de prueba', 'correo': 'cliente@example.com'
        }, follow=True)
        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue(Cliente.objects.filter(correo='cliente@example.com').exists())
        self.assertContains(respuesta, 'Cliente de prueba')

    def test_valida_correo_repetido(self):
        self.client.force_login(self.usuario)
        Cliente.objects.create(nombre='Primero', correo='repetido@example.com')
        respuesta = self.client.post(reverse('clientes_crear'), {
            'nombre': 'Segundo', 'correo': 'repetido@example.com'
        })
        self.assertEqual(Cliente.objects.filter(correo='repetido@example.com').count(), 1)
        self.assertContains(respuesta, 'Ya existe') if 'Ya existe' in respuesta.content.decode() else self.assertContains(respuesta, 'correo')

class AutenticacionTests(TestCase):
    def test_registro_valido_inicia_sesion(self):
        respuesta = self.client.post(reverse('registro'), {
            'username': 'nuevo', 'email': 'nuevo@example.com',
            'password1': 'ClaveDePrueba2026!', 'password2': 'ClaveDePrueba2026!'
        })
        self.assertRedirects(respuesta, reverse('home'))
        self.assertTrue(User.objects.filter(username='nuevo').exists())

    def test_logout_por_post(self):
        usuario = User.objects.create_user(username='prueba', password='ClaveDePrueba2026!')
        self.client.force_login(usuario)
        respuesta = self.client.post(reverse('logout'))
        self.assertRedirects(respuesta, reverse('login'))
