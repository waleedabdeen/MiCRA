import { useState } from 'react';
import ClassifierForm from '../../components/ClassifierForm/ClassifierForm';
import { Steps } from 'antd';
import LabelsSelector from '../../components/LabelsSelector/LabelsSelector';
import Tracer from '../../components/Tracer/Tracer';

const TracingPage = () => {
    const [current, setCurrent] = useState(0);
    const [source, setSource] = useState();
    const [labels, setLabels] = useState([]);
    const [selectedLabels, setSelectedLabels] = useState([]);

    const onTextChange = () => {
        setLabels([]);
        setSelectedLabels([]);
        setSource();
    };

    const onStepChange = (value) => {
        setCurrent(value);
    };

    const onClassificationComplete = (req, labels) => {
        setSource(req)
        setLabels(labels);
        selectedLabels([]);
        setCurrent(1);
    };

    const onLabelsSelectionComplete = (selectedLabels) => {
        setSelectedLabels(selectedLabels);
        setCurrent(2);
    };

    return (
        <Steps
            current={current}
            onChange={onStepChange}
            direction="vertical"
            items={[
                {
                    title: 'Step 1: Classification',
                    description: (<ClassifierForm onComplete={onClassificationComplete} onTextChange={onTextChange} />)
                },
                {
                    title: 'Step 2: Labels Selection',
                    description: (<LabelsSelector labels={labels} onComplete={onLabelsSelectionComplete} />)
                },
                {
                    title: 'Step 3: Trace',
                    description: (<Tracer labels={selectedLabels} source={source} />),
                },
            ]}
        />
    );
}

export default TracingPage;
