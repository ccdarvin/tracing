import '../styles/globals.css'


export default function Layout({ children }: { children: React.ReactNode }) {

  return <html lang="es">
    <head></head>
    <body>
      {children}
    </body>
  </html>
}