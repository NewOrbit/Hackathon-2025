# Frontend (Vite + React + MUI)

A minimal React frontend scaffolded with Vite, TypeScript, and MUI.

## Prerequisites

- Node.js 18+
- npm (or pnpm/yarn)

## Install

```bash
cd src/frontend
npm install
```

## Develop

```bash
npm run dev
```

Then open the URL shown in the terminal (typically http://localhost:5173).

## Lint

```bash
npm run lint
```

## Build

```bash
npm run build
```

Preview the production build locally:

```bash
npm run preview
```

## Tech stack

- React 19 + TypeScript
- Vite (rolldown-vite)
- MUI 7 for UI components
- ESLint + Prettier

## Project structure

```
src/frontend
├─ src/
│  ├─ App.tsx           # Root component (MUI Stack example)
│  ├─ main.tsx          # React root + CssBaseline
│  └─ index.css         # Global styles
├─ package.json         # Scripts and dependencies
├─ tsconfig*.json       # TypeScript configs
└─ eslint.config.js     # ESLint setup
```

## Customization

- Update `App.tsx` to add pages or components.
- Add a MUI theme provider if you want custom theming.
- Integrate with MCP backends by adding fetch calls or a small client.
