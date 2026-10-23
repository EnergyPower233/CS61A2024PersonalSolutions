(define (curry-cook formals body) (if (null? formals) body `(lambda (,(car formals)) ,(curry-cook (cdr formals) body))))

(define (curry-consume curry args)
 (if (null? args) curry (curry-consume (curry (car args)) (cdr args))))

(define-macro (switch expr options)
  (switch-to-cond (list 'switch expr options)))


;?
(define (switch-to-cond switch-expr)
  (cons `cond
        (map ;生成列表
        ; Build a list.
              (lambda (option)
               (cons ;组装
               ; Assemble.
               `(equal? ,(car (cdr switch-expr)) ,(car option)) ;此乃 bool
               ; This is a boolean.
               (cdr option)));把上面的那行和这个组了 是cond的一个情况
               ; Combine the previous line with this one; it becomes one cond clause.
             (car (cdr (cdr switch-expr))))));这是所有options
             ; This covers all options.
