void vTask1( void *pvParameters )
{
    const char* const message = "buzz\r\n";
    for ( ;; ) {
        /* buzzを出力 */
        vPrintString( message );
    }
    /* タスクは基本的に無限ループで実装されなければいけません。 */
    /* タスクを終了させたいときはタスクの終了前にvTaskDeleteを読んでタスクを削除する必要があります。 */
    vTaskDelete(NULL); // NULLを渡すと現在実行中のタスクを削除します
}

void vTask2( void *pvParameters )
{
    const char* const message = "fizz\r\n";
    for ( ;; ) {
        /* fizzを出力 */
        vPrintString( message );
    }
}

int main( void )
{
    /**/
    xTaskCreate(
        vTask1, /* タスクとして実行する関数への関数ポインタ */
        "Task 1",/* タスク名です。デバッグのために設定されます。 */
        1000, /* タスクに割り当てられるスタックのサイズ */
        NULL, /* タスクに渡される引数へのポインタ */
        1, /* タスクの優先度。大きいほど優先的に実行されます。 */
        NULL ); /* 生成されたタスクへのハンドラです。タスクの優先度を変更する際に使われます。ハンドラが不要な場合はNULLを指定します。 */

    /* タスク2を生成します。 */
    xTaskCreate( vTask2, "Task 2", 1000, NULL, 1, NULL );

    /* タスクの実行を始めます。 */
    vTaskStartScheduler();

    /*main関数は最後まで到達してはいけません。そこで、無限ループを挿入します。 */
    for ( ;; );
}