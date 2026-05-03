Plan: add frontend test support

1. Install test dependencies
   - In `frontend`, install:
     - `vitest`
     - `@testing-library/react`
     - `@testing-library/jest-dom`
     - `@testing-library/user-event`
     - `@types/testing-library__jest-dom`

2. Add test scripts to `frontend/package.json`
   - `test`: run unit tests once
   - `test:watch`: run tests in watch mode
   - `coverage`: run tests with coverage output
   - Example:
     - `"test": "vitest run"`
     - `"test:watch": "vitest"`
     - `"coverage": "vitest run --coverage"`

3. Configure Vitest in `frontend/vite.config.ts`
   - Add a `test` block:
     - `environment: 'jsdom'`
     - `globals: true`
     - `setupFiles: './src/setupTests.ts'`
     - `include: ['src/**/*.{test,spec}.{js,ts,tsx}']`

4. Add a test setup file
   - Create `frontend/src/setupTests.ts`
   - Add `import '@testing-library/jest-dom'`

5. Add initial test files
   - Create a smoke test in `frontend/src/pages/__tests__` or `frontend/src/__tests__`
   - Example: `AlbumDetailPage.test.tsx` or `ManagementPage.test.tsx`
   - Verify the component renders and key UI text appears

6. Verify with Yarn
   - `cd frontend`
   - `yarn test`
   - `yarn test:watch`
   - `yarn coverage`

Outcome
- `yarn test` will work for the frontend.
- The app becomes testable with modern Vite tooling.
- This plan matches the current Vite + React + TypeScript structure.
