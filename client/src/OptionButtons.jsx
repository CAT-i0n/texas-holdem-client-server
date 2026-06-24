import { VIEW_BOX_SIZE } from "./Consts";

export function OptionButtons({ options, send_data }) {
    let elements = []
    for (const option in options) {
        switch (option) {
            case 'raise':
            case 'bet':
                var currentValue = 0
                elements.push(<div className="action">
                    <input type="range" orient="vertical" className="slider" id='raise-slider'
                        min={options[option][0]}
                        max={options[option][1]}
                        onChange={(e) => {
                            const val = e.target.value;
                            document.getElementById('raise-button').innerHTML = `${option}<br>${val}`
                        }}
                        defaultValue={options[option][0]} />
                    <button id='raise-button'
                        className="action-button"
                        onClick={() => send_data(option, document.getElementById("raise-slider").value)}>
                        {option}<br/>{options[option][0]}
                    </button>
                </div>)
                break;
            default:
                elements.push(<div className="action">
                    <button className="action-button" onClick={() => send_data(option)}>{option}</button>
                </div>);

        }

    }
    return (
        <foreignObject
            x={VIEW_BOX_SIZE.x - 250} y={-50} width={VIEW_BOX_SIZE.x} height={VIEW_BOX_SIZE.y}>
            <div style={{
                display: 'flex',
                flexDirection: 'column',
                height: '100%',
                width: '100%',
                backgroundColor: 'transparent',
            }}>
                <div style={{
                    height: '100%',
                    width: '100%',
                    display: 'flex',
                    flexDirection: 'row',
                    gap: '2%',
                    backgroundColor: 'transparent',
                    alignItems: 'flex-end'
                }}>
                    {elements}
                </div>
            </div>
        </foreignObject>
    )
}