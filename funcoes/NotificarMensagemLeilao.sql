CREATE OR REPLACE FUNCTION notifyOnBoardPost()
	RETURNS TRIGGER
LANGUAGE 'plpgsql'
AS $BODY$
declare
    f record;
	f2 record;
	msg text;
	dt TIMESTAMP;
	novoId bigint;
	c1 cursor(idPessoa bigint) for
        select *
        from pessoa
        where pessoa.id=idPessoa;
	c2 cursor(idPessoa bigint,idNotificacao bigint) for
        select *
        from notificacao_pessoa
        where notificacao_pessoa.pessoa_id=idPessoa and notificacao_pessoa.notificacao_id=idNotificacao;
begin
    open c1(new.pessoa_id);
	fetch c1 into f2;
	close c1;
	msg:='O licitador ' || f2.nome || ' escreveu no moral do leilao ' || new.leilao_id || ': ' || new.titulo;
	dt:= CURRENT_TIMESTAMP;
	insert into notificacao(mensagem,data) values (msg,dt) returning id into novoId;
	for f in 
		select * from PeopleInAuctionBoard(new.leilao_id)
		union
		select * from PeopleInAuctionLicitations(new.leilao_id)
    loop 
		insert into notificacao_pessoa(lida,notificacao_id,pessoa_id) values(FALSE,novoId,f.id);
    end loop;
	for f in 
		select * from leilao where leilao.id=new.leilao_id
    loop 
		open c2(f.pessoa_id,novoId);
		fetch c2 into f2;
		close c2;
		if(not found) then
			insert into notificacao_pessoa(lida,notificacao_id,pessoa_id) values(FALSE,novoId,f.pessoa_id);
		end if;
    end loop;
	return new;
end;
$BODY$;

DROP TRIGGER IF EXISTS notifyOnBoardPost
  ON mensagem;
CREATE TRIGGER notifyOnBoardPost 
   after insert
   ON mensagem
   FOR EACH ROW
       EXECUTE PROCEDURE notifyOnBoardPost();
