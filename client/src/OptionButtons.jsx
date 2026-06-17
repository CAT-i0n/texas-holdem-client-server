export function OptionButtons({ options, send_data }) {
    let buttons = []
    for (const option in options) {
        switch (option) {
            case 'raise':
            case 'bet':
                var currentValue = 0
                buttons.push(<div key={option}>
                    <button onClick={() => send_data(option, document.getElementById('raise-value').textContent)}>{option}</button>
                    <span id='raise-value'> {options[option][0]}</span>
                    <div>
                        <input type="range"
                            min={options[option][0]}
                            max={options[option][1]}
                            onChange={(e) => {
                                const val = e.target.value;
                                document.getElementById('raise-value').textContent = val;
                            }}
                            defaultValue={options[option][0]} className="slider" id="myRange" />
                    </div>
                </div>);
                break;
            default:
                buttons.push(<button onClick={() => send_data(option)}>{option}</button>);
        }

    }
    return (
        <div style={{
            display: 'flex',
            flexDirection: 'row',
            gap: '10px',
            overflowX: 'auto'
        }}>
            {buttons}
        </div>
    )
}