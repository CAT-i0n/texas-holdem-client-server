import { VIEW_BOX_SIZE } from "./Consts";

export function OptionButtons({ options, send_data }) {
    let elements = []
    for (const option in options) {
        switch (option) {
            case 'raise':
            case 'bet':
                var currentValue = 0
                elements.push(<button className="action" onClick={() => send_data(option, document.getElementById('raise-value').textContent)}>{option}</button>)
                elements.push(
                    <input type="range" orient="vertical"
                        min={options[option][0]}
                        max={options[option][1]}
                        onChange={(e) => {
                            const val = e.target.value;
                            document.getElementById('raise-value').textContent = val;
                        }}
                        defaultValue={options[option][0]} id="myRange"/>)
                elements.push(<span className="raise-num" id='raise-value'> {options[option][0]}</span>)
                break;
            default:
                elements.push(<button className="action" onClick={() => send_data(option)}>{option}</button>);
        }

    }
    return (
        <foreignObject
            x={750} y={-90} width={1000} height={VIEW_BOX_SIZE.y}>
            <div style={{
                display: 'flex',
                flexDirection: 'column',
                height: '100%',
                width: '100%',
                backgroundColor: 'transparent',
            }}>
                <div style={{
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'row',
                    gap: '1%',
                    backgroundColor: 'transparent',
                    alignItems: 'flex-end'
                }}>
                    {elements}
                </div>
            </div>
        </foreignObject>
    )
}