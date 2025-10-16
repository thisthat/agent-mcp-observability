import { trace, } from '@opentelemetry/api';
import { AlwaysOnSampler, SimpleSpanProcessor, } from '@opentelemetry/sdk-trace-base';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-proto';
import { resourceFromAttributes } from '@opentelemetry/resources';
import { ATTR_SERVICE_NAME, } from '@opentelemetry/semantic-conventions';
import fs from 'fs';
import { NodeSDK } from '@opentelemetry/sdk-node';
export const setupTracing = (serviceName) => {
    const api = fs.readFileSync('/etc/secrets/token').toString().trim();
    const exporter = new OTLPTraceExporter({
        url: "https://xbw95514.dev.dynatracelabs.com/api/v2/otlp/v1/traces",
        headers: {
            'Authorization': `Api-Token ${api}`
        }
    });
    const sdk = new NodeSDK({
        resource: resourceFromAttributes({
            [ATTR_SERVICE_NAME]: serviceName,
        }),
        spanProcessors: [new SimpleSpanProcessor(exporter)],
        traceExporter: exporter,
        sampler: new AlwaysOnSampler(),
        instrumentations: [],
    });
    sdk.start();
    return trace.getTracer(serviceName);
};
