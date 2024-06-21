var signals={}

function Derived_From(id, func) {
    var signal={"Id":id, "Value":func, "onChange":()=>{}, "setValue":(value)=>{
        signals[id].onChange()
        signals[id].value=()=>value
    }}
    signals[id]=signal
    return signal
}

function Signal(id, value) {
    var signal={"Id":id, "Value":()=>value, "onChange":()=>{}, "setValue":(value)=>{
        signals[id].onChange()
        signals[id].Value=()=>value
    }}
    signals[id]=signal
    return signal
}

export {Signal, Derived_From}