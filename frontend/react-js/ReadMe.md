# React JS – Topic-Wise Questions (Complete Coverage)

---

## Table of Contents

- [1️⃣ React Fundamentals](#1-react-fundamentals-foundation)
- [2️⃣ Components & Rendering](#2-components--rendering)
- [3️⃣ Props & State](#3-props--state-core-react)
- [4️⃣ Events & Forms](#4-events--forms)
- [5️⃣ Hooks – Basics](#5-hooks--basics-must-know)
- [6️⃣ Hooks – Advanced](#6-hooks--advanced)
- [7️⃣ Rendering, Reconciliation & Virtual DOM](#7-rendering-reconciliation--virtual-dom)
- [8️⃣ Lists, Keys & Performance](#8-lists-keys--performance)
- [9️⃣ Context API & State Management](#9-context-api--state-management)
- [🔟 Routing (React Router)](#-routing-react-router)
- [1️⃣1️⃣ Data Fetching & API Integration](#11-data-fetching--api-integration)
- [1️⃣2️⃣ Performance Optimization](#12-performance-optimization-advanced)
- [1️⃣3️⃣ Error Handling & Stability](#13-error-handling--stability)
- [1️⃣4️⃣ Security & Best Practices](#14-security--best-practices)
- [1️⃣5️⃣ Build, Deployment & Production](#15-build-deployment--production)
- [1️⃣6️⃣ Testing in React](#16-testing-in-react)
- [1️⃣7️⃣ React Architecture & Design Thinking](#17-react-architecture--design-thinking)

---

<a id="1-react-fundamentals-foundation"></a>
## 1️⃣ React Fundamentals (Foundation)
1.	What is React and why was it created?
2.	What problem does React solve compared to vanilla JS?
3.	Is React a framework or a library?
4.	What are the core principles of React?
5.	What is JSX?
6.	Why JSX is not HTML?
7.	How JSX gets converted to JavaScript?
8.	What is Babel’s role in React?
9.	What is ReactDOM?
10.	What happens when you call ReactDOM.createRoot()?
---

<a id="2-components-rendering"></a>
## 2️⃣ Components & Rendering
1.	What is a component in React?
2.	Difference between functional and class components?
3.	Why are functional components preferred today?
4.	What is component reusability?
5.	What is component composition?
6.	What is conditional rendering?
7.	How does React decide when to re-render a component?
8.	What is a pure component?
9.	What are controlled vs uncontrolled components?
---

<a id="3-props-state-core-react"></a>
## 3️⃣ Props & State (Core React)
1.	What are props?
2.	Are props mutable or immutable?
3.	What is state?
4.	Difference between props and state?
5.	Why state updates are asynchronous?
6.	What happens internally when state changes?
7.	Why should we never mutate state directly?
8.	What is lifting state up?
9.	What is derived state and why it’s dangerous?
---

<a id="4-events-forms"></a>
## 4️⃣ Events & Forms
1.	How event handling works in React?
2.	Why React uses synthetic events?
3.	Difference between React events and native DOM events?
4.	How to handle form submission in React?
5.	Controlled vs uncontrolled inputs?
6.	How to manage multiple inputs with one handler?
7.	How validation is handled in React forms?
8.	How to prevent default behavior in React events?
---

<a id="5-hooks-basics-must-know"></a>
## 5️⃣ Hooks – Basics (Must-Know)
1.	What are Hooks?
2.	Why Hooks were introduced?
3.	Rules of Hooks – why are they strict?
4.	What is useState?
5.	What is useEffect?
6.	How useEffect replaces lifecycle methods?
7.	What is dependency array?
8.	What happens if dependency array is empty?
9.	Cleanup function in useEffect – why needed?
10.	Common mistakes with useEffect?
---

<a id="6-hooks-advanced"></a>
## 6️⃣ Hooks – Advanced
1.	What is useRef and why it exists?
2.	Difference between useRef and useState?
3.	What is useMemo?
4.	What problem does useMemo solve?
5.	What is useCallback?
6.	useMemo vs useCallback?
7.	What is useReducer?
8.	useState vs useReducer – when to use?
9.	What are custom hooks?
10.	Why custom hooks improve code quality?
---

<a id="7-rendering-reconciliation-virtual-dom"></a>
## 7️⃣ Rendering, Reconciliation & Virtual DOM
1.	What is Virtual DOM?
2.	Why React does not use real DOM directly?
3.	What is reconciliation?
4.	How React compares Virtual DOM trees?
5.	What are keys and why are they important?
6.	What happens if keys are missing or incorrect?
7.	How React batches updates?
8.	What is Strict Mode in React?
9.	Why components render twice in Strict Mode?
---

<a id="8-lists-keys-performance"></a>
## 8️⃣ Lists, Keys & Performance
1.	How to render lists in React?
2.	Why keys must be stable and unique?
3.	Index as key – why is it risky?
4.	How React optimizes list rendering?
5.	What causes unnecessary re-renders?
6.	How to prevent unnecessary re-renders?
7.	What is memoization in React?
8.	What is React.memo?
---

<a id="9-context-api-state-management"></a>
## 9️⃣ Context API & State Management
1.	What problem does Context API solve?
2.	What is prop drilling?
3.	How Context works internally?
4.	When should NOT use Context?
5.	Context vs Redux?
6.	How Context causes re-renders?
7.	Best practices for Context usage?
8.	How to optimize Context performance?
---

<a id="10-routing-react-router"></a>
## 🔟 Routing (React Router)
1.	Why routing is needed in SPA?
2.	What is client-side routing?
3.	How React Router works internally?
4.	Difference between BrowserRouter & HashRouter?
5.	What is dynamic routing?
6.	What are route params?
7.	What is nested routing?
8.	Protected routes – how to implement?
9.	What is lazy loading routes?
---

<a id="11-data-fetching-api-integration"></a>
## 1️⃣1️⃣ Data Fetching & API Integration
1.	How to fetch data in React?
2.	Where should API calls be made?
3.	fetch vs axios?
4.	How to handle loading & error states?
5.	What is async/await in React?
6.	How to cancel API requests?
7.	What is debouncing and throttling?
8.	How to handle pagination?
9.	Infinite scrolling – how it works?
---

<a id="12-performance-optimization-advanced"></a>
## 1️⃣2️⃣ Performance Optimization (Advanced)
1.	What causes slow React applications?
2.	What is code splitting?
3.	What is lazy loading?
4.	How React.lazy works?
5.	What is Suspense?
6.	How to optimize large lists?
7.	How to measure performance in React?
8.	What is Profiler?
9.	When memoization hurts performance?
---

<a id="13-error-handling-stability"></a>
## 1️⃣3️⃣ Error Handling & Stability
1.	What are error boundaries?
2.	Why error boundaries exist?
3.	What errors error boundaries cannot catch?
4.	How to create an error boundary?
5.	Global error handling strategies?
6.	How to handle runtime vs API errors?
7.	Best practices for production error handling?
---

<a id="14-security-best-practices"></a>
## 1️⃣4️⃣ Security & Best Practices
1.	Is React secure by default?
2.	What is XSS and how React prevents it?
3.	What is dangerouslySetInnerHTML?
4.	How to secure API tokens?
5.	Environment variables in React?
6.	Why .env variables are public?
7.	Common security mistakes in React apps?
---

<a id="15-build-deployment-production"></a>
## 1️⃣5️⃣ Build, Deployment & Production
1.	What happens during npm run build?
2.	Development vs production build?
3.	What is tree shaking?
4.	How React app is deployed?
5.	CDN role in React deployment?
6.	How caching works for React apps?
7.	How to handle environment-based configs?
8.	How React app behaves on refresh?
---

<a id="16-testing-in-react"></a>
## 1️⃣6️⃣ Testing in React
1.	Why testing is important in React?
2.	Unit vs integration testing?
3.	What is React Testing Library?
4.	What should we test in React?
5.	How to test components with hooks?
6.	How to mock API calls?
7.	Snapshot testing – good or bad?
8.	Testing best practices?
---

<a id="17-react-architecture-design-thinking"></a>
## 1️⃣7️⃣ React Architecture & Design Thinking
1.	How to structure a React project?
2.	Container vs presentational components?
3.	Feature-based vs layer-based structure?
4.	How React fits in micro-frontend architecture?
5.	React with BFF pattern?
6.	How React scales in large applications?
7.	Common architectural mistakes?

