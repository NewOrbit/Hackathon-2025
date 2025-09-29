## Travel Packing List Generator — Implementation Plan

### Goal
Build an AI assistant that generates an optimized travel packing list and optional booking suggestions, taking into account user constraints (e.g., backpack capacity), trip parameters (destination, time of day, dates, trip length), weather, attraction plans, and regulatory requirements (airport security, visas, documents). Use the same agent/tooling pattern as `src/agent/attractions.ipynb` with MCP tools over HTTP and LangChain agent.

### Scope Overview
- **Core**: Conversational packing list generation that factors in weather, trip length, time-of-day activities, transportation type, and user capacity constraints. Validate against security rules and travel document requirements. Summarize suggested bookings and ask for explicit confirmation before any booking action.
- **Integrations**: Reuse existing MCPs (`weather`, `attractions`) and add new MCPs for travel requirements and bookings.
- **Phase 2 (optional/next)**: Backpack photo analysis to estimate capacity and determine which items fit using a simplified volume/packing algorithm with a vision-enabled model.

## User Stories
- As a traveler, I can specify destination, dates, trip length, planned activities and time-of-day usage so the assistant tailors my packing list.
- As a traveler, I can set constraints like backpack capacity, airline baggage limits, weight targets, or liquid restrictions to get a feasible list.
- As a traveler, I receive alerts if items violate airport security, require declarations, or if I need visas/documents.
- As a traveler, I can see weather-informed suggestions (layers, rain gear) and trip-length-based quantities.
- As a traveler, I can receive suggested bookings (flights/hotels/attractions), and the system will only book after I confirm.
- As a traveler (Phase 2), I can upload a photo of my backpack to estimate volume and check if the packing list fits.
- As a traveler, I can enable a "keep-it-simple" mode to get a concise, printable checklist I can use 3 minutes before leaving the house.
- As a traveler, the assistant proactively asks for my carry capacity, max weight I can comfortably carry, and any limitations (mobility, health, liquid restrictions) and tailors recommendations accordingly.

## Functional Requirements
- **Input collection**: destination(s), dates, trip length, activities (day/night, hiking, formal, beach, business), transport (flight/airline), accommodations, personal preferences (laundry, style), constraints (capacity in L, max weight, budget), and known documents.
  - Agent now collects these interactively in chat mode before generating advice, and auto-extracts details (origin city, destination, start date) from natural language.
- **Onboarding questions**: explicitly ask for backpack capacity (L), maximum comfortable carry weight (kg), airline/route, cabin class, mobility/health limitations (e.g., knee issues, need for meds), liquid constraints, and laundry availability.
  - Chat flow prompts for number of adults, children, infants, and pets, confirming each before proceeding.
- **Weather intake**: fetch current and forecast weather (reuse `weather` MCP) for relevant dates.
- **Attractions intake**: optional attraction plans (reuse `attractions` MCP) to bias item categories (e.g., museum vs hiking).
- **Regulatory checks**: identify prohibited/restricted items (airport), visa requirements, passport validity, entry paperwork, vaccinations where applicable.
- **List generation**: produce a categorized packing list with quantities, rationale, estimated volume/weight, and flags for restricted items.
- **Capacity/weight fit**: adjust list to meet capacity/weight limits; propose alternatives (e.g., travel-size liquids, laundry mid-trip).
- **Booking suggestions**: propose relevant bookings; show structured summary; require explicit confirmation before calling booking tools.
- **Explainability**: show which constraints and data influenced each recommendation.
- **Item categorization and filters**: classify each item by safety status (safe/restricted/prohibited), priority (must-have/nice-to-have), weight class (light/medium/heavy), and category (clothing/toiletries/electronics/documents/health/accessories). Allow filtering/sorting and provide totals per class.
- **Keep-it-simple mode**: output a minimal, printable checklist (plain text/markdown) with only item names, quantities, and a short high-priority notes section. Skip long explanations and avoid non-essential tool calls.
  - CLI `simple` command now uses `simple_checklist` responses.
- **Budgeting and costs (Phase 1.5)**: capture user budgets (overall, per-category like clothing/toiletries, and per booking type), estimate packing vs buy-at-destination tradeoffs, compute baggage fees risk based on weight/size, and include price ranges from mocked MCPs in summaries.
  - Status: implementation in progress with mocked data; live integrations deferred to Phase 2.

## Non-Functional Requirements
- **Safety**: never perform bookings without explicit user confirmation. Flag uncertainties and provide sources for regulatory advice.
- **Privacy**: minimize PII retention; redact sensitive inputs in logs.
- **Reliability**: degrade gracefully when some MCPs are unavailable (fallbacks and clear messages).
- **Latency**: batch MCP calls where possible (weather + restrictions queries in parallel).
- **Token efficiency**: cap max tokens per response, summarize chat history aggressively, truncate irrelevant memory, and limit tool-call fan-out. Prefer structured terse outputs in keep-it-simple mode. Refuse off-topic tasks to avoid token waste.
- **Scope/guardrails**: the assistant is strictly for travel planning/packing. Politely refuse unrelated domains; avoid medical/legal advice beyond linking to official sources; disallow dangerous or disallowed items; rate-limit excessively long prompts and enforce message length caps.
- **Offline-first (Phase 1)**: default to strict offline/mock mode with zero external HTTP. Any attempt to call live endpoints should raise a clear error.
- **LLM integration**: DeepseekTravels defaults to the LangChain Azure OpenAI agent whenever required env vars are set; falls back to deterministic mock engine otherwise. System prompt resides in `src/agent/prompts/system_prompt.txt` and includes interactive onboarding instructions. MCP endpoints for weather, attractions, and travel requirements are configurable via environment variables.

## Architecture Overview (patterned after `src/agent/attractions.ipynb`)
Replicate the notebook structure with analogous cells:
1) Env and dependency setup (uv + pip) → same approach as in `attractions.ipynb`.
2) Imports and dotenv loading → include LangChain, Azure OpenAI, MCP adapter (`MultiServerMCPClient`, `load_mcp_tools`).
3) MCP HTTP client config → include servers: `weather`, `attractions`, `travel_requirements`, `booking`.
4) Tool loading via MCP adapter → `await mcp_client.get_tools()`.
5) Agent setup → `AzureChatOpenAI` + `create_tool_calling_agent` + `ConversationBufferMemory`.
6) Initialization cell → runs `await initialize_agent()`; logs available tools.
7) User input/processing → `process_user_input` prints intermediate steps/tools used.
8) Connectivity test cell → lists tools with descriptions.
9) Example usage cell → demonstrate a few end-to-end prompts.
10) Interactive chat loop → optional (confirmations and iterative constraints refinement).
11) Cleanup cell → close the MCP client.

Additionally, provide a console script entrypoint so the same orchestration can run outside of Jupyter (see "Runtime Form Factor").

## MCP Servers and Tools
Reuse existing:
- `weather-mcp`: `get_current_weather`, `get_weather_forecast` (already present)
- `attractions-mcp`: optional for itinerary-driven packing

Add new MCPs:
- **Phase 1 HTTP policy**: Maintain deterministic behavior by standing up mock MCP servers for weather, requirements, and booking. Only budgeting still relies on in-process fixtures; a future `budgeting-mcp` will complete MCP coverage.
1) `travel-requirements-mcp` (HTTP)
   - **Purpose**: Validate airport security restrictions, baggage rules, visas, documents.
   - Tools:
     - `get_airport_security_rules(airport_code, country_code, airline, cabin_class)` → returns prohibited/restricted items (e.g., liquids > 100ml, batteries), quantity limits, references.
     - `check_baggage_allowance(airline, cabin_class, route, fare_brand)` → size, linear dimensions, weight limits, personal item policy, references.
     - `get_visa_requirements(nationality, destination_country, transit_countries, stay_length_days, purpose)` → visas/ESTA/eTA, passport validity, entry docs, references.
     - `get_documents_checklist(destination_country, nationality, minors_traveling, driving, insurance)` → documents and recommended paperwork.
   - **Status**: Implemented in `src/mcp/requirements-mcp` with mock fixtures identical to the in-app mock client. Connected through `MultiServerMCPClient` for both CLI fallback and LangChain agent paths.

2) `booking-mcp` (HTTP)
   - **Purpose**: Search and propose bookings; perform booking only with explicit confirmation.
   - Tools:
     - `search_flights(origin, destination, depart_date, return_date, passengers, cabin_class, budget)`
     - `search_hotels(destination, check_in, check_out, guests, budget, preferences)`
     - `search_activities(destination, dates, interests, budget)`
     - `hold_booking(booking_type, booking_payload)` → returns hold ID and expiration; requires confirmation step.
     - `confirm_booking(hold_id, payment_token_or_redirect)` → only after user says “confirm”.
   - **Status**: Implemented in `src/mcp/booking-mcp` and accessed via MCP throughout the application.

Data contracts (illustrative JSON schemas):

```json
{
  "generatePackingListRequest": {
    "destination": "string",
    "dates": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
    "tripLengthDays": 6,
    "activities": ["hiking", "museum", "beach", "business_dinner"],
    "timeOfDayUsage": ["day", "night"],
    "transport": {"mode": "flight", "airline": "UA", "cabinClass": "economy"},
    "accommodation": {"hasLaundry": true},
    "constraints": {"capacityLiters": 28, "maxWeightKg": 8, "liquidLimitMl": 100},
    "preferences": {"style": "casual", "tech": true, "photography": false},
    "travelerProfile": {"nationality": "PL", "age": 35}
  }
}
```

```json
{
  "packingListItem": {
    "category": "clothing|toiletries|electronics|documents|health|accessories",
    "name": "Merino T-shirt",
    "qty": 3,
    "estimatedVolumeL": 0.9,
    "estimatedWeightKg": 0.45,
    "weightClass": "light|medium|heavy",
    "priority": "must_have|nice_to_have",
    "safetyStatus": "safe|restricted|prohibited",
    "flags": ["liquid_over_limit", "battery_wh", "sharp_object"],
    "reason": "6 days with laundry once",
    "restricted": false,
    "alternatives": ["synthetic tee"]
  }
}
```

## Packing Logic and Constraints
- **Trip length scaling**: base quantities with diminishing increments and laundry factor (e.g., shirts = ceil(tripDays/2) with laundry once).
- **Time of day**: add night items (headlamp, reflective layer, evening wear), sun items for daytime (sunglasses, sunscreen).
- **Short trips**: for sub-day or single-day daytime outings, skip multi-day essentials (e.g., multiple socks/underwear) unless users opt in or overnight usage is stated.
- **Weather**: from forecast; choose layers, rain gear, insulation; heat adds hydration kit and light fabrics.
- **Activities**: hiking → boots, socks, poles; beach → swimwear, quick-dry towel; business → formal attire.
- **Transport**: airline baggage allowance and security rules filter/flag items; auto-replace oversized liquids with travel-size.
- **Capacity/weight fit**: greedy plus knapsack heuristic by value/volume to respect `capacityLiters` and `maxWeightKg`; suggest renting/buying at destination for low-utility bulky items.
- **Regulatory checks**: call `travel-requirements-mcp` tools; remove or flag disallowed items, add document checklist, surface references.
- **Categorization**: assign `safetyStatus`, `priority`, and `weightClass` using rules + MCP responses; compute totals per class and show trade-offs (e.g., remove nice-to-have heavy items first when over capacity).
- **Explainability**: attach a short reason per item and a global summary of constraints that drove changes.

## Agent Prompt and Guardrails
- System prompt emphasizes: obey constraints, verify with requirements tools, show rationale, and ask before booking or removing critical documents.
- The agent must present a delta if the list changes due to capacity or regulations.
- All booking actions must go through a confirmation ask: “Do you want me to place a hold/confirm?”
- Add explicit scope rules: refuse non-travel topics; keep answers concise unless asked to expand; prefer bullet lists; in keep-it-simple mode output a single concise checklist.
- Add token budget instructions: summarize context after each turn, cap tool calls per turn (e.g., ≤4), and prefer reusing cached results.
- Identity: refer to the assistant as "DeepseekTravels" in system prompt and user-facing output headers.

## Notebook Plan (`src/agent/packing_list.ipynb`)
Create a new notebook mirroring the `attractions.ipynb` cell structure:
1) Kernel + uv setup cell.
2) Imports + dotenv + MCP adapter imports.
3) MCP client setup with servers: `weather`, `attractions`, `travel-requirements`, `booking`.
4) `create_mcp_tools()` to load tools and print list.
5) `setup_agent()` with `AzureChatOpenAI`, tools array, and a tailored system prompt.
6) `initialize_agent()` async cell to build the agent and log tools.
7) `process_user_input()` with intermediate tool call logging.
8) `test_mcp_connection()` to enumerate tools and descriptions.
9) Example usage cells:
   - Basic packing request with constraints.
   - Request that triggers security/visa checks and shows flagged items.
   - Booking suggestion flow that stops for confirmation.
   - Keep-it-simple checklist for a last-minute departure.
10) Optional `chat_loop()` for interactive demos.
11) `cleanup_mcp()` to close connections.

## Detailed Step-by-Step Implementation
1) Define new MCP services
   - Create `src/mcp/travel-requirements-mcp/` with HTTP server exposing the four tools listed above; implement providers: government sites, airline baggage policies, and security guidelines with cached reference links.
   - Create `src/mcp/booking-mcp/` with HTTP server exposing search/hold/confirm endpoints; wire to sandbox/mock providers (phase 1) with clear “DEMO ONLY” flags.
   - Provide `pyproject.toml`, `README.md`, `models.py`, and `utils.py` similar to existing MCP packages for weather/attractions.
   - Phase 1: implement in-memory fixtures and deterministic responses; disable any outbound HTTP at the server layer; include a toggle for later live mode but keep default OFF.

2) Data modeling
   - Define Pydantic models for requests/responses in each MCP, including references/links and confidence fields.
   - Standardize units (L, kg, ml) and add conversion helpers.

3) Packing engine module
   - Implement a deterministic rule + heuristic layer to convert inputs to items with qty/volume/weight and reasons.
   - Add a capacity/weight fitter (value-per-volume heuristic; optional 0/1 knapsack for key categories), emitting alternatives and trade-offs.

4) Agent prompt engineering
   - Create a clear system prompt with objectives, constraints, tool usage order (parallel where possible), and confirmation gate for bookings.
   - Add few-shot examples for day/night decisions, trip-length scaling, and restriction enforcement.

5) Notebook build (`packing_list.ipynb`)
   - Copy the structure from `attractions.ipynb` and adapt the text and logs to the packing flow.
   - Ensure verbose intermediate step printing to aid demo/debugging.
   - Name the agent in outputs as "DeepseekTravels".

6) Confirmation UX
   - Agent presents a structured booking summary (price, dates, refund policy) and asks for explicit confirmation.
   - On “confirm”, call `hold_booking` → `confirm_booking`; otherwise, discard.

7) Testing
   - Unit tests for packing engine edge cases (short vs long trips, extreme weather, strict capacity).
   - Integration tests calling MCP stubs (mocked responses) for requirements and bookings.
   - Notebook walkthrough with 3–4 realistic scenarios.

8) Observability and safety
   - Add tool call logging, timing, and error surfaces in the notebook.
   - Redact PII in logs; store only non-sensitive context.

## Runtime Form Factor: Console App now, UI-ready later
- Provide a Python console script `deepseek_travels_cli.py` that invokes the same agent orchestration as the notebook.
- Use Typer or argparse for a clean CLI: modes `assist` (interactive), `generate` (one-shot packing list), `simple` (keep-it-simple checklist), and `book` (suggest/confirm flow).
- Decouple I/O from logic: CLI calls a service layer (`PackingAssistantService`) so a future UI (web/desktop/mobile) can reuse the same API.
- Stream outputs to console with minimal token usage; enable `--verbose` for debugging.
- Enforce mocks in Phase 1: default flags `--offline` and `--use-mocks` enabled; reject `--live` until Phase 2.

## Phase 1 Offline/Mock Mode
- Default runtime is offline: all integrations use stubs/fixtures.
- Environment flags and CLI switches:
  - Env: `DEEPSEEKTRAVELS_OFFLINE=true`, `DEEPSEEKTRAVELS_USE_MOCKS=true` (default)
  - CLI: `--offline/--no-offline`, `--use-mocks/--no-use-mocks` (Phase 1 forces these to true)
- Add a network guard that raises if any HTTP client attempts a live call in Phase 1.

## Proposed Folder Structure and Solution Architecture
```
src/
  agent/
    packing/                    # domain logic (packing engine, fitters, rules)
      __init__.py
      engine.py
      fitters.py
      rules.py
    models/                     # pydantic models and schemas
      __init__.py
      packing_models.py
      requirements_models.py
    prompts/
      __init__.py
      system_prompt.txt         # includes DeepseekTravels identity and guardrails
    services/
      __init__.py
      assistant_service.py      # PackingAssistantService orchestrating tools + engine
      mcp_clients.py            # thin clients using langchain_mcp_adapters
    cli/
      deepseek_travels_cli.py   # console entrypoint (Typer/argparse)
    packing_list.ipynb          # demo notebook mirroring attractions.ipynb
  mcp/
    travel-requirements-mcp/
      ...                       # HTTP MCP server (tools: security, baggage, visa, docs)
    booking-mcp/
      ...                       # HTTP MCP server (tools: search/hold/confirm)
tests/
  unit/
    test_engine_scaling.py
    test_fitters_constraints.py
    test_categorization.py
  integration/
    test_requirements_mcp_stub.py
    test_booking_mcp_stub.py
  e2e/
    test_cli_simple_mode.py
    test_cli_full_flow.py
```

Architecture layers:
- Interface: CLI (and Jupyter for demos)
- Orchestrator: `PackingAssistantService` (LangChain Agent + memory + tools)
- Domain: Packing engine (rules + heuristics + fitters) and models
- Integrations: MCP clients for weather, attractions, travel requirements, booking
- Config: `.env` parsing and runtime options
- Observability: structured logging for tool calls and decisions

## Phase 1.5: Cost Assessment and Budgeting
- Objectives:
  - Gather budgets: overall trip budget, luggage budget (baggage fees), per-category budgets (optional), and booking budgets (flights/hotels/activities).
  - Estimate costs with mocks: item purchase-at-destination ranges, travel-size alternatives, laundry costs, baggage fee thresholds, and booking price ranges.
  - Optimize packing list within capacity and budget: prefer lower-cost alternatives where utility similar; flag over-budget categories and suggest trade-offs.
- Implementation notes:
  - Use mocked price catalogs and fee tables in MCPs and/or local fixtures; no live HTTP.
  - Add a simple cost model: total_estimated_cost = items_to_buy_cost + expected_baggage_fees + laundry_cost + booking_estimates (if selected).
  - Present a budget summary with deltas after any list change.
  - Respect keep-it-simple mode by showing only totals and top 3 cost drivers.
  - All costs labeled as estimates with mock/source notes.

## Phase 2: Vision-Based Backpack Fit
- **Objective**: Given a backpack photo, estimate capacity and determine if the recommended list fits.
- **Approach**:
  - Use an Azure OpenAI vision-capable model to analyze the image; optionally prompt user for dimensions/known volume for calibration.
  - Estimate interior volume (L) from detected dimensions/shape; fallback to user-provided specs.
  - Assign volume to items based on category and compressibility; run a simplified 3D bin/knapsack fit.
  - Return: items that fit, items that do not, recommended swaps (e.g., packable jacket, travel-size toiletries).
- **MCP**: `vision-mcp` with tools `estimate_backpack_volume(photo_url|upload)` and `fit_items_to_backpack(items, volume_liters)`.
- **Limitations**: Explain estimation uncertainty; recommend manual measurement for high confidence.

## Example Conversations to Support
- “Trip to Tokyo for 6 days in November, lots of evening events, 28L backpack, economy on ANA.”
- “Weekend beach trip to Lisbon, 20L daypack, can do laundry.”
- “Patagonia trek 10 days, check security restrictions for stove fuel and trekking poles.”
- “What flights and hotels would you suggest for my Paris dates? Hold but don’t confirm yet.”

## Env and Config
- Reuse `.env` style variables as in `attractions.ipynb`: `AZURE_OPENAI_*`, and new MCP URLs: `TRAVEL_REQUIREMENTS_MCP_URL`, `BOOKING_MCP_URL`.
- Keep `uv` package management in the notebook to ensure kernel uses `.venv`.
- Phase 1 defaults: `DEEPSEEKTRAVELS_OFFLINE=true`, `DEEPSEEKTRAVELS_USE_MOCKS=true`.

## Risks and Mitigations
- **Regulatory accuracy**: Always return references; label outputs as guidance and encourage official verification.
- **Overfitting to capacity**: Provide alternatives and allow user overrides; offer destination purchase options.
- **Booking liability**: Use sandbox/mock providers in demos; require explicit confirmation; show clear costs and policies.
- **Vision accuracy** (Phase 2): Communicate uncertainty and ask for manual dimensions when needed.

## Milestones
1) Week 1: `travel-requirements-mcp` + packing engine prototype + notebook skeleton, with ALL HTTP calls mocked and offline.
2) Week 2: `booking-mcp` mock integration + end-to-end demo in notebook.
3) Week 3: Phase 1.5 budgeting: add mocked price catalogs, baggage fee tables, laundry costs; integrate budget inputs and summaries.
4) Week 4: Tests, polishing, and documentation; add sample scenarios.
5) Phase 2: Vision MCP and fit feature (timeboxed spike then refine).

## Feasibility Review and Suggested Improvements
- Feasibility: High. The pattern is aligned with `attractions.ipynb` and reuses MCP adapters. New MCPs can start with mock/sandbox providers. Packing engine is a bounded rules + heuristics problem.
- Risks: regulatory data freshness; booking provider variability; capacity estimation accuracy. Mitigate by including references, mocks first, and user confirmations.
- Improvements:
  - Add caching layer for weather and requirements queries to save tokens.
  - Introduce profiles (business, backpacking) to preload defaults for faster onboarding.
  - Add export formats: markdown, CSV, and printable PDF for the checklist.
  - Optional weight scale integration: let users input measured bag weight to refine fit.

## Acceptance Criteria
1) CLI `DeepseekTravels` runs with `--help` and supports modes: `assist`, `generate`, `simple`, `book`.
2) Onboarding prompts collect capacity (L), max carry weight (kg), airline/route, cabin class, limitations, and dates/activities; can also be passed via flags.
3) Weather MCP and Travel Requirements MCP are called (or mocked) and their results influence the list (e.g., rain gear added; liquids >100ml flagged).
4) Output includes categorization: `safetyStatus`, `priority`, `weightClass`, and per-category totals; respects `capacityLiters` and `maxWeightKg`.
5) Keep-it-simple mode emits a concise, printable checklist with quantities in ≤ one screen/page and avoids non-essential tool calls.
6) Booking suggestions are presented with price/dates/policies, and no booking is performed without explicit “confirm”.
7) Token guardrails: responses ≤ configured token budget; limited parallel tool calls; de-duplication and caching of repeated queries.
8) Off-topic requests are politely refused with scope explanation.
9) Errors from unavailable MCPs degrade gracefully with actionable guidance.
10) Unit, integration, and E2E tests pass; sample scenarios produce expected outputs.
11) Phase 1 mock enforcement: all external HTTP is mocked/stubbed; tests verify that any live HTTP attempt raises.

## Testing Plan
- Unit tests
  - Trip-length scaling math and laundry adjustments.
  - Weather-driven item inclusion (rain, heat, cold) and time-of-day logic.
  - Capacity/weight fitter: verify removal order (heavy nice-to-have first), alternatives, and totals.
  - Categorization rules: safety, priority, weight class and flags.
- Integration tests (with mocked MCPs)
  - Requirements MCP: prohibited items flagged/removed; visa/doc checklist attached.
  - Booking MCP: search returns suggestions; hold requires confirmation; confirm only on explicit user command.
  - Weather MCP: forecast alters layers and accessories.
- End-to-end tests
  - CLI simple mode outputs minimal checklist within token and line limits.
  - CLI full flow generates categorized list, asks confirmations, and respects constraints.
  - Failure cases: missing MCPs, network timeouts, and off-topic prompts.
- Performance/Token tests
  - Ensure context summarization is invoked; large histories remain within budget.
- Security/Scope tests
  - Off-topic requests refused; dangerous items flagged; no auto-booking.
 - Mock/offline tests
  - Verify that any attempt to issue live HTTP calls results in a controlled error in Phase 1.
  - Validate stub data coverage for weather, requirements, and booking flows.

1) Week 1: `travel-requirements-mcp` + packing engine prototype + notebook skeleton, with ALL HTTP calls mocked and offline.
2) Week 2: `booking-mcp` mock integration + end-to-end demo in notebook.
3) Week 3: Tests, polishing, and documentation; add sample scenarios.
4) Phase 2: Vision MCP and fit feature (timeboxed spike then refine).


