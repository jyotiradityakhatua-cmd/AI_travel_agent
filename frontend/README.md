# AI Travel Planner Frontend

This React application is built with Vite and TypeScript as the frontend for the AI Travel Planner project. It includes:

- AI-inspired destination recommendations
- Drag-and-drop itinerary builder
- Booking hub with curated flight and hotel offers
- User authentication flow and protected routes

## Structure

- `src/App.tsx` — top-level routing and page composition
- `src/components/` — reusable page and UI components
- `src/hooks/useAuth.ts` — simple auth state management
- `src/styles/global.css` — layout, theme, and responsive styling

## Local development

1. Install dependencies

   ```bash
   cd frontend
   npm install
   ```

2. Start the app

   ```bash
   npm run dev
   ```

3. Open the app at `http://localhost:3000`

## Backend integration

The backend API is assumed to run at `http://localhost:8000`.

### API endpoints (next step)

- `POST /chat/register` — create user account
- `POST /chat/login` — authenticate user
- `POST /chat/` — send chat message and receive AI response stream
- `GET /chat/history/{chat_id}` — fetch chat history
- `GET /chat/users/{user_id}/chats` — fetch saved conversations

## Deployment

Build the production bundle with:

```bash
npm run build
```

Then serve the `dist/` folder using any static web server.

## Design assumptions

- Travel enthusiasts want a modern, highly visual planner
- Users expect mobile-responsive and accessible workflows
- AI should feel like a helpful assistant rather than a generic search

## Notes

- The app currently uses local mock data for recommendations and bookings
- Authentication is a local state placeholder; integrate backend login/register in the next phase
