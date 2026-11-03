# Rumo à Posse

Plataforma gratuita de estudo para concursos públicos: questões reais com gabarito oficial, comentários (os escritos por IA vêm marcados), simulados, revisão espaçada e aulas gratuitas do YouTube tocando na própria página.

- Site: https://02q1.github.io/rumo-a-posse/
- Progresso salvo no Supabase (login por link no e-mail). Cada pessoa só lê e grava o próprio registro (RLS em `supabase/schema.sql`).
- A chave do Supabase no `index.html` é a publicável (pública por definição); a chave secreta nunca vai para este repositório.
