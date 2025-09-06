import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import { EventBusProvider } from './patterns/observer/EventBus'
import { EnrollmentProvider } from './state/EnrollmentContext'


ReactDOM.createRoot(document.getElementById('root')!).render(
<React.StrictMode>
    <BrowserRouter>
        <EventBusProvider>
            <EnrollmentProvider>
                <App /> 
            </EnrollmentProvider>
        </EventBusProvider>
    </BrowserRouter>
</React.StrictMode>
)