sequenceDiagram
    participant S as System/User
    participant P as Procd
    participant I as Init Script
    S->>P: Start Service
    P->>I: Call 'init'
    I->>P: procd_add_instance
    P-->>S: Service Running
