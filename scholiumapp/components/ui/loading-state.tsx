"use-client";
import { Card, Spinner } from "@radix-ui/themes";
import React from 'react';
export default function LoadingState({ message}: { message?: string }) {
    return (
        <Card className="flex items-center justify-center gap-2 p-3">
            <div className="flex flex-row items-center gap-2">
                <Spinner size="2" />
                <span>{message}</span>
            </div>
        </Card>
    );
}