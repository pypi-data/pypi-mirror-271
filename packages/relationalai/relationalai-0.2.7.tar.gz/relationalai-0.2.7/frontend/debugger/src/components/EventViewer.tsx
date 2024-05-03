import { Dynamic } from "solid-js/web";
import { Machine } from "./Schematic";
import { Message, Placeholder, Span, Subject } from "../debugger_client";
import "./EventViewer.styl";
import { For, JSXElement, Show, splitProps } from "solid-js";
import { CodeBlock } from "./ui/Code";
import { omit } from "@src/util";

export namespace View {
    export interface EventViewProps<T extends Subject> {
        subject: T;
    }

    export function Compilation(props: EventViewProps<Message.Compilation>) {
        const mech = () => props.subject.parent?.mech!
        return (
            <span-viewer class={`block ${props.subject.span_type}`}>
                <Show when={mech()}>
                    <section class="grow">
                        <Machine machine={mech()} />
                    </section>
                </Show>
                <section>
                    <h3>{props.subject?.source.file}: {props.subject?.source.line}</h3>
                    <CodeBlock lang="python">{props.subject?.source.block}</CodeBlock>
                </section>
                <section>
                    <CodeBlock lang="rel">
                        {props.subject?.emitted}
                    </CodeBlock>
                </section>
                <section>
                    <h3>IR</h3>
                    <CodeBlock>
                        {props.subject.task}
                    </CodeBlock>
                </section>
            </span-viewer>
        )
    }

    export function InstallBatch(props: EventViewProps<Message.Time>) {
        return (
            <span-viewer class="time install-batch">
                <CodeBlock lang="rel">
                    {props.subject?.code}
                </CodeBlock>
            </span-viewer>
        )
    }

    export function QueryResult(props: EventViewProps<Message.Time>) {
        const results = () => props.subject.results;
        return (
            <span-viewer class="time query-result">
                <Show when={results()}>
                    <section>
                        <h3>Results ({results()?.values.length} / {results()?.count})</h3>
                        <table>
                            <thead>
                                <tr>
                                    <For each={Object.keys(results()?.values[0] ?? {})}>
                                        {(key) => <td>{key}</td>}
                                    </For>
                                </tr>
                            </thead>
                            <tbody>
                                <For each={results()?.values}>
                                    {(row) => (
                                        <tr>
                                            <For each={Object.entries(row)}>
                                                {([key, value]) => <td>{value}</td>}
                                            </For>
                                        </tr>
                                    )}
                                </For>
                            </tbody>
                        </table>
                    </section>
                </Show>
            </span-viewer>
        )
    }

    export function Placeholder(props: EventViewProps<Subject>) {
        return (
            <span-viewer class="placeholder">
                Waiting for block {props.subject.selection_path.slice(1)}
            </span-viewer>
        );
    }

    export function UnknownSpan(props: EventViewProps<Span>) {
        const attrs = () => {
            return omit(props.subject, "event", "parent", "selection_path", "events", "mech")
        }

        const content = () => JSON.stringify(attrs(), null, 4)
        return (
            <span-viewer>
                <CodeBlock lang="json">
                    {content()}
                </CodeBlock>
                <For each={props.subject.events}>
                    {(event) => <EventViewer subject={event} />}
                </For>
            </span-viewer>
        )
    }

    export function Unknown(props: EventViewProps<Subject>) {
        const attrs = () => {
            return omit(props.subject, "parent", "selection_path")
        }
        const content = () => JSON.stringify(attrs(), null, 4)
        return (
            <span-viewer>
                <CodeBlock lang="json">
                    {content()}
                </CodeBlock>
            </span-viewer>
        )
    }
}

export interface EventViewerProps {
    subject: Subject;
}
export function EventViewer(props: EventViewerProps) {
    const component = () => {
        const subject = props.subject;
        if(subject.event === "placeholder") return View.Placeholder;
        if(Message.is_time(subject)) {
            if(subject.type === "install_batch") return View.InstallBatch;
            if(subject.type === "query") return View.QueryResult;
        }
        if(subject.event === "compilation") return View.Compilation;
        if(Span.is_span(subject)) return View.UnknownSpan;
        return View.Unknown;
    };

    return (
        <Dynamic component={component()} subject={props.subject as any} />
    )
}
