import { Message, Span, client, type Subject } from "@src/debugger_client"
import { Component, For, Show, children, createEffect, createSignal, untrack, useContext, type JSXElement } from "solid-js"
import { Collapsible } from "./ui/Collapsible";
import { EventListSelection } from "@src/Selection";
import { Dynamic } from "solid-js/web";
import { CodeBlock } from "./ui/Code";
import "./EventList.styl";
import { fmt, prefix_of } from "@src/util";
import { Icon } from "./ui/Icon";

//------------------------------------------------------------------------------
// EventList
//------------------------------------------------------------------------------

export interface EventListProps {
    events: (Message.Event | Span)[],
    sub?: boolean
}
export function EventList(props: EventListProps) {
    return (
        <div class={`event-list ${props.sub ? "sub" : ""}`}>
            <For each={props.events}>
                {(event) => <EventListItem event={event} />}
            </For>
        </div>
    )
}

export function EventListItem(props: EventListItemProps) {
    const component = (() => {
        const event = props.event;
        if (Span.is_program(event)) return EventItemProgram;
        // if (Span.is_block(event)) return EventItemBlock;
        else if (Span.is_span(event)) return EventItemUnknownSpan;
        else if (Message.is_compilation(event)) return EventItemCompilation;
        else if (Message.is_time(event)) return EventItemTime;
        else return EventItemUnknown;

    }) as () => Component<EventListItemProps>;

    return (
        <Dynamic component={component()} event={props.event} selects={props.selects} />
    )
}

//------------------------------------------------------------------------------
// Base components for event list items
//------------------------------------------------------------------------------

export interface EventListItemProps<T extends Subject = Subject> {
    event: T,
    selects?: Subject
}

interface EventListBranchProps<T extends Span = Span> extends EventListItemProps<T> {
    class?: string;
    children?: JSXElement;
    open?: boolean;
}
export function EventListBranch<T extends Span>(props: EventListBranchProps<T>) {
    const klass = () => `event-list-item branch ${props.event.event} ${props.event.span_type || ""} ${props.class || ""}`;

    const selection = useContext(EventListSelection);
    const contains_selection = () => selection.selected().some((subject) => {
        const subject_path = subject.selection_path;
        const span_path = props.event.selection_path;
        if(subject_path.length < span_path.length) return false;
        for(let ix = 0; ix < span_path.length; ix += 1) {
            if(subject_path[ix] !== span_path[ix]) return false;
        }
        return true;
    });

    const [open, set_open] = createSignal(contains_selection());

    createEffect(() => {
        let should_be_open = contains_selection();
        if (untrack(() => open()) !== should_be_open) {
            set_open(should_be_open);
        }
    });

    return (
        <Collapsible side="top" open={open()} onOpenChange={set_open} class={klass()}>
            <Collapsible.Trigger as="header">
                <Collapsible.TriggerIcon />
                {props.children}
            </Collapsible.Trigger>
            <Collapsible.Content>
                <EventList sub events={props.event.events} />
            </Collapsible.Content>
        </Collapsible>
    );
}

interface EventListLeafProps<T extends Subject = Subject> extends EventListItemProps<T> {
    class?: string;
    children?: JSXElement;
}
export function EventListLeaf(props: EventListLeafProps<Subject>) {
    const selection = useContext(EventListSelection);
    const is_selected = () => selection.is_selected(props.selects ?? props.event);
    const klass = () => `event-list-item leaf ${props.event.event} ${props.event.span_type || ""} ${props.class || ""} ${is_selected() ? "selected" : ""}`;
    const onclick = () => selection?.select?.(props.selects ?? props.event);
    return (
        <div class={klass()} onclick={onclick}>
            {props.children}
        </div>
    );
}

//------------------------------------------------------------------------------
// Items
//------------------------------------------------------------------------------

export function EventItemProgram(props: EventListItemProps<Span.Program>) {
    const selection = useContext(EventListSelection);
    const is_selection_inside = () => !!selection.selected().find(item => prefix_of(item.selection_path, props.event.selection_path));
    const should_open = () => is_selection_inside() || client.latest() === props.event;
    return (
        <EventListBranch event={props.event} open={should_open()} class="naked">
            <span class="event-label">Run #{(props.event as Span.Program).run}</span>

            <span class="event-detail">
                {props.event.main}
            </span>
            <span style="flex: 1" />
            <span>
                <Show when={props.event.elapsed} fallback={<Icon name="clock-play" />}>
                    {fmt.time.s(props.event.elapsed!)}
                </Show>
            </span>
        </EventListBranch>
    )
}

export function EventItemCompilation(props: EventListItemProps<Message.Compilation>) {
    let source = () => props.event?.source;

    return (
        <Show when={source()?.block}>
            <EventListLeaf event={props.event} class="block naked" selects={props.selects}>
                <header>
                    <span style="flex: 1" />
                    <span class="event-detail">
                        <span class="file">{source()?.file}</span>
                        <span class="sep">:</span>
                        <span class="line">{source()?.line}</span>
                    </span>
                </header>
                <CodeBlock lang="python" dense no_copy>
                    {source()?.block}
                </CodeBlock>
            </EventListLeaf>
        </Show>
    )
}

export function EventItemTime(props: EventListItemProps<Message.Time>) {
    return (
        <EventListLeaf event={props.event} selects={props.selects}>
            <span class="event-label">
                {props.event.type}
            </span>
            <span style="flex: 1" />
            <span class="event-detail">
                {fmt.time.ms(props.event.elapsed * 1000)}
            </span>
        </EventListLeaf>
    )
}

export function EventItemUnknownSpan(props: EventListItemProps<Span>) {
    const selection = useContext(EventListSelection);
    const is_selected = () => selection.is_selected(props.selects ?? props.event);
    const klass = () => `event-list-item branch unknown ${is_selected() ? "selected" : ""}`;
    const content = children(() => (
        <For each={props.event.events}>
            {(event) => <EventListItem event={event} selects={props.selects} />}
        </For>
    ));
    return (
        <Show when={content.toArray()?.filter((v) => v).length}>
            <div class={klass()}>
                {content()}
            </div>
        </Show>
    )
}

export function EventItemUnknown(props: EventListItemProps<Message.Event>) {
    return (
        <EventListLeaf event={props.event} class="unknown" selects={props.selects}>
            <span>
                {props.event.event}
            </span>
            <span>
                {Message.is_time(props.event) ? props.event.type : undefined}
            </span>
        </EventListLeaf>
    )
}


