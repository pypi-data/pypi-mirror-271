import { For, Match, Show, Switch, createEffect, createSignal } from "solid-js";
import { EventListSelection, Selection } from "./Selection";
import { EventList } from "./components/EventList";
import { EventViewer } from "./components/EventViewer";
import { Sidebar } from "./components/Sidebar";
import { Button } from "./components/ui/Button";
import { Field, Format } from "./components/ui/Field";
import { Icon } from "./components/ui/Icon";
import { Modal } from "./components/ui/Modal";
import { Tooltip } from "./components/ui/Tooltip";
import { Message, Span, client, get_in, type Subject } from "./debugger_client";
import "./App.styl";
import { Breadcrumbs } from "./components/ui/Breadcrumbs";
import { unwrap } from "solid-js/store";

function App() {
    const event_list_selection = new Selection<Subject>("EventList");

    const clear = () => {
        client.connection.disconnect();
        event_list_selection.clear()
        client.clear();
    };

    const [pinned, set_pinned] = createSignal<boolean>(true);

    createEffect((prev_len: number|undefined) => {
        const cur_len = client.spans().length;
        const cur = event_list_selection.primary();
        if (pinned() && cur_len !== prev_len && cur) {
            event_list_selection.select({ event: "placeholder", selection_path: [cur_len - 1, ...cur.selection_path.slice(1)] })
        }
        return cur_len;
    });

    createEffect(() => {
        let selected = event_list_selection.primary();
        if (selected?.event === "placeholder") {
            let available = get_in(client.root, selected.selection_path);
            if(available) {
                event_list_selection.select(available);
            }
        }
    });

    return (
        <EventListSelection.Provider value={event_list_selection}>
            <app-chrome>
                <Sidebar side="left" defaultOpen>
                    <header>
                        <Button class="icon" onclick={clear} tooltip="clear events">
                            <Icon name="ban" />
                        </Button>
                        <Button class="icon" tooltip="Follow last run" onclick={() => set_pinned(v => !v)}>
                            <Icon name="pin" type={pinned() ? "filled" : "outline"} />
                        </Button>
                        <span style="flex: 1" />
                        <Modal title="Settings" content={<Settings />}>
                            <Modal.Trigger as={Button} class="icon" tooltip="settings">
                                <Icon name="settings" />
                            </Modal.Trigger>
                        </Modal>
                    </header>
                    <EventList events={client.spans()} />
                </Sidebar>
                <main>
                    <Show when={event_list_selection.primary()}>
                        <EventBreadcrumbs subject={event_list_selection.primary()!} select={event_list_selection.select} />
                        <scroll-container>
                            <scroll-inner>
                                <EventViewer subject={event_list_selection.primary()!} />
                            </scroll-inner>
                        </scroll-container>
                    </Show>
                </main>
                <Status />
            </app-chrome>
        </EventListSelection.Provider>
    );
};

export default App;

function Status() {
    return (
        <Tooltip content={client.connected() ? "Connected to program" : "Disconnected from program"}>
            <Tooltip.Trigger as="status-icon">
                <Show when={client.connected()} fallback={<Icon name="antenna-bars-off" />}>
                    <Icon name="antenna-bars-5" />
                </Show>
            </Tooltip.Trigger>
        </Tooltip>
    )
}


function Settings() {
    return (
        <>
            <section>
                <h3>Connection</h3>
                <Field.Number label="Polling Interval" formatOptions={Format.seconds} minValue={1}
                    defaultValue={client.connection.reconnectInterval / 1000}
                    onRawValueChange={(v) => client.connection.reconnectInterval = v * 1000} />
                <Field.Text label={"Debug URL"} placeholder={"ws://localhost:1234"}
                    defaultValue={client.connection.ws_url} onChange={(v) => client.connection.ws_url = v} />
            </section>

        </>
    )
}

interface EventBreadcrumbsProps {
    subject: Subject,
    select?: (subject: Subject) => any,
}
function EventBreadcrumbs(props: EventBreadcrumbsProps) {
    const crumbs = () => {
        let cur: Subject|undefined = props.subject;
        let crumbs = [];
        while(cur) {
            const item = cur;
            if(Span.is_span(item) && item.span_type === "root") {
                break;
            }
            crumbs.unshift(
                <Breadcrumbs.Item onClick={() => props.select?.(item!)}>
                    <Switch>
                        <Match when={Span.is_span(item) && item.span_type === "program"}>
                            run {(item as Span.Program).run}
                        </Match>
                        <Match when={Span.is_span(item)}>
                            {(item as Span).span_type}
                        </Match>
                        <Match when={Message.is_time(item)}>
                            {(item as Message.Time).type} result
                        </Match>
                        <Match when={true}>
                            {(item as Message.Time).event}
                        </Match>
                    </Switch>
                </Breadcrumbs.Item>
            );
            cur = cur.parent;
        }
        return crumbs;
    }

    return (
        <Breadcrumbs>
            {crumbs()}
        </Breadcrumbs>
    )
}
